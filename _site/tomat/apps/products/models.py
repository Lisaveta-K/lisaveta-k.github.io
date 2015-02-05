# -*- coding: utf-8 -*-

import uuid
import os.path
import datetime
import logging

import prices
from django.db import models
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save, post_delete
from satchless.item import Item
from pytils.translit import slugify
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from products.managers import ProductManager


logger = logging.getLogger(__name__)

EMPTY_OBJECT = object()


def category_cover_upload_to(instance, filename):
    return 'categories/covers/%(name)s%(ext)s' % {
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1].lower(),
    }


def category_icon_upload_to(instance, filename):
    return 'categories/icons/%(name)s%(ext)s' % {
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1].lower(),
    }


class Category(MPTTModel):
    """Категория товаров"""

    parent = TreeForeignKey('self', related_name='children', null=True, blank=True,
        verbose_name=u'Родительская категория')
    title = models.CharField(u'Название', max_length=255)
    slug = models.SlugField(u'Алиас', unique=True)
    cover = models.ImageField(u'Изображение', upload_to=category_cover_upload_to, blank=True,
        help_text=u'Важно, чтобы изображение было квадратным, с белым или прозрачным фоном')
    icon = models.ImageField(u'Иконка', upload_to=category_icon_upload_to, blank=True,
        help_text=u'Выводится в меню')
    description = models.TextField(u'Описание', blank=True)
    is_complementary = models.BooleanField(u'Сопутствующие товары', default=False, db_index=True,
        help_text=u'Например: шары, упаковка, открытки')
    complementary_cover = models.ImageField(u'Изображение 1', upload_to=category_cover_upload_to,
        blank=True, null=True, help_text=u'Важно, чтобы изображение было квадратным, с белым или прозрачным фоном')
    complementary_hover_cover = models.ImageField(u'Изображение 2', upload_to=category_cover_upload_to,
        blank=True, null=True, help_text=u'Показывается при наведении мышкой')
    is_standalone = models.BooleanField(u'Показывать в меню отдельным блоком с картинкой', default=False, db_index=True)
    is_visible = models.BooleanField(u'Публикуется', default=True, db_index=True)
    show_cover_in_menu = models.BooleanField(u'Показывать картинку в меню', default=True,
        help_text=u'Если включена галочка «показывать в меню отдельным блоком», но не нужно выводить картинку')
    position = models.PositiveIntegerField(u'Позиция', default=0)
    legacy_id = models.CommaSeparatedIntegerField(u'ID старого сайта', null=True, blank=True,
        help_text=u'Можно несколько через запятую', max_length=255)
    is_signable = models.BooleanField(u'Подпись к товарам', default=False,
        help_text=u'Например, к открыткам в корзине можно будет оставить подпись')

    class Meta:
        db_table = 'products_categories'
        verbose_name = u'категорию'
        verbose_name_plural = u'категории'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        if not self.parent_id:
            return 'products.views.categories.parent', (self.slug, ), {}
        return 'products.views.categories.read', (self.get_root().slug, self.slug), {}

    def bottom_descendants(self):
        return self.get_descendants().filter(level=2, is_visible=True).prefetch_related('parent')

    def direct_children(self):
        return Category.objects.filter(parent=self, is_visible=True).order_by('position')

    def length_class(self):
        return (len(self.title) / 5) * 5 + 5


class Product(models.Model, Item):
    """Товар магазина"""

    # Список полей, используемых при выводе товара в списке
    # Используется в методе .only() queryset'a
    LIST_ITEM_REQUIRED_FIELDS = ('title', 'price', 'discount', 'wholesale_price', 'wholesale_discount',
        'franchisee_price', 'franchisee_discount', 'is_new')

    title = models.CharField(u'Название', max_length=255)
    description = models.TextField(u'Описание', blank=True)
    code = models.CharField(u'Код 1С', help_text=u'Код товара в базе 1С, например «УТ000006411»',
        max_length=20, blank=True, null=True, db_index=True)
    sku = models.CharField(u'Артикул', max_length=30, null=True, blank=True, db_index=True)

    price = models.DecimalField(u'Розничная цена', max_digits=8, decimal_places=2, db_index=True, null=True, blank=True)
    discount = models.DecimalField(u'Розничная цена со скидкой', max_digits=8, decimal_places=2, null=True, blank=True)
    wholesale_price = models.DecimalField(u'Оптовая цена', max_digits=8, decimal_places=2, db_index=True, null=True, blank=True,
        help_text=u'Цена за единицу')
    wholesale_discount = models.DecimalField(u'Оптовая цена со скидкой', max_digits=8, decimal_places=2, null=True, blank=True)
    franchisee_price = models.DecimalField(u'Франчайзинговая цена', max_digits=8, decimal_places=2, db_index=True, null=True, blank=True,
        help_text=u'Цена за единицу')
    franchisee_discount = models.DecimalField(u'Франчайзинговая цена со скидкой', max_digits=8, decimal_places=2, null=True, blank=True)

    is_visible = models.BooleanField(u'Публикуется', default=False, db_index=True)
    is_new = models.BooleanField(u'Новый', default=False, db_index=True)
    is_retail = models.BooleanField(u'Розничный товар', default=False, db_index=True,
        help_text=u'Показывается розничным покупателям')
    is_wholesale = models.BooleanField(u'Оптовый товар', default=False, db_index=True,
        help_text=u'Показывается только оптовикам и франчайзи')

    weight = models.PositiveIntegerField(u'Вес', help_text=u'в граммах', null=True, blank=True)
    dimensions = models.CharField(u'Размер', max_length=15, help_text=u'в сантиметрах', blank=True)
    pack_amount = models.PositiveSmallIntegerField(u'Количество в упаковке', default=1,
        help_text=u'Показывается только оптовикам и франчайзи')
    box_amount = models.PositiveSmallIntegerField(u'Количество упаковок в коробке', blank=True, null=True,
        help_text=u'Показывается только оптовикам и франчайзи')

    quantity = models.PositiveIntegerField(u'Остаток на складе', default=0)
    wholesale_quantity = models.PositiveIntegerField(u'Оптовый остаток', default=0)
    wholesale_legacy_id = models.CharField(max_length=20, blank=True, null=True, editable=False)

    categories = TreeManyToManyField(Category, related_name='products', verbose_name=u'Категории')

    created = models.DateTimeField(u'Дата появления', default=datetime.datetime.now)
    updated = models.DateTimeField(u'Дата последнего редактирования', editable=False, default=datetime.datetime.now,
        auto_now=True)

    search_index = VectorField()

    objects = ProductManager()

    class Meta:
        db_table = 'products_items'
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'

    def __unicode__(self):
        return self.title

    @property
    def slug(self):
        return slugify(self.title)

    def get_price_per_item(self, **kwargs):
        if not 'request' in kwargs:
            raise ImproperlyConfigured('`request` object should be in the kwargs')
        price = self.price_for_user(kwargs['request'].user)
        return prices.Price(price or 0, currency='RUB')

    def get_quantity(self, **kwargs):
        return 1

    def get_absolute_url(self):
        cache_key = 'products.product.%d.get_absolute_url' % self.id
        url = cache.get(cache_key, EMPTY_OBJECT)
        if not url is EMPTY_OBJECT:
            logger.debug('Product #%d got a cached value for get_absolute_url method: %s' % (self.id, url))
        else:
            logger.debug('Product #%d got an empty cache value for get_absolute_url method' % (self.id,))
            try:
                category = self.categories.all()[0]
            except IndexError:
                url = None
            else:
                root = category.get_root()

                url = reverse('products.views.products.read', args=(root.slug, category.slug, self.id, self.slug))

            cache.set(cache_key, url, 3600)
            logger.debug('Product %d updated cache for get_absolute_url method: %s' % (self.id, url))

        return url

    def get_main_photo(self):
        try:
            return self.photos.filter(is_main=True)[0]
        except IndexError:
            try:
                photo = self.photos.all()[0]
                self.photos.filter(id=photo.id).update(is_main=True)

                return photo
            except IndexError:
                return

    def price_for_user(self, user):
        if user.is_authenticated():
            if user.is_wholesale:
                return self.wholesale_discount or self.wholesale_price
            elif user.is_franchisee:
                return self.franchisee_discount or self.franchisee_price

        return self.discount or self.price

    def has_discount(self, user):
        if user.is_authenticated():
            if user.is_wholesale:
                if self.wholesale_discount and self.wholesale_price:
                    return True
            elif user.is_franchisee:
                if self.franchisee_discount and self.franchisee_price:
                    return True

        return self.discount and self.price

    def available_for_user(self, user):
        if not self.is_visible:
            return False

        if user.is_anonymous() and not self.is_retail:
            return False

        if user.is_authenticated():
            if user.show_wholesale() and not self.is_wholesale:
                return False
            if not user.show_wholesale() and not self.is_retail:
                return False

        return True

    def is_signable(self):
        return any(self.categories.values_list('is_signable', flat=True))


def photo_upload_to(instance, filename):
    return 'products/%(product_id)d/%(name)s%(ext)s' % {
        'product_id': instance.product_id,
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1].lower(),
    }


class Photo(models.Model):
    product = models.ForeignKey(Product, related_name='photos')
    image = models.ImageField(upload_to=photo_upload_to, verbose_name=u'Изображение')
    is_main = models.BooleanField(u'Главная', default=False, db_index=True)
    legacy_hash = models.CharField(max_length=40, editable=False)

    class Meta:
        db_table = 'products_photos'
        verbose_name = u'Фотография'
        verbose_name_plural = u'Фотографии'
        index_together = (
            ('product', 'is_main'),
        )


# Чистим кэш при сохранении любой модели
_cache_clean_func = lambda *args, **kwargs: cache.clear()
for model_cls in (Category, Product, Photo):
    post_save.connect(_cache_clean_func, sender=model_cls)
    post_delete.connect(_cache_clean_func, sender=model_cls)
