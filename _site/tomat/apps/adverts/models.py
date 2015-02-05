# -*- coding: utf-8 -*-

import uuid
import os.path

from django.db import models

from adverts.managers import CouponManager
from products.models import Category, Product


def promo_image_upload_to(instance, filename):
    return 'adverts/promo/%(name)s%(ext)s' % {
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1],
    }


class Promo(models.Model):
    """Промо-блок"""

    title = models.CharField(u'Название', max_length=255)
    color = models.CharField(u'Цвет фона', max_length=6)
    is_retail = models.BooleanField(u'Показывать рознице', default=False, db_index=True)
    is_wholesale = models.BooleanField(u'Показывать опту', default=False, db_index=True)
    image = models.ImageField(u'Изображение', upload_to=promo_image_upload_to,
        help_text=u'Высота изображения - 350 пикселей, ширина неограничена. Рекомендуется до 2100 пикселей с плавным переходом в однородный фон')
    url = models.URLField(u'Ссылка')
    position = models.PositiveIntegerField(u'Позиция', default=0)

    categories = models.ManyToManyField(Category, related_name='promos', blank=True, verbose_name=u'Категории')

    class Meta:
        db_table = 'adverts_promos'
        verbose_name = u'промо-блок'
        verbose_name_plural = u'промо-блоки'

    def __unicode__(self):
        return self.title


class Coupon(models.Model):
    """Промо-код"""

    TYPE_ALL = 0
    TYPE_RETAIL = 1
    TYPE_WHOLESALE = 2

    TYPES_CHOICES = (
        (TYPE_ALL, u'Все товары'),
        (TYPE_RETAIL, u'Розничные'),
        (TYPE_WHOLESALE, u'Оптовые'),
    )

    code = models.CharField(u'Код', max_length=20)

    date_start = models.DateField(u'Дата начала действия')
    date_end = models.DateField(u'Дата окончания действия')

    discount_percent = models.PositiveSmallIntegerField(u'Скидка в процентах', null=True, blank=True)
    discount_amount = models.PositiveIntegerField(u'Скидка в рублях', null=True, blank=True)

    discount_level = models.PositiveIntegerField(u'Определенная сумма заказа', null=True, blank=True,
        help_text=u'Скидка будет действовать, если сумма заказа выше этого числа')

    categories = models.ManyToManyField(Category, verbose_name=u'Категории', blank=True)
    products = models.ManyToManyField(Product, verbose_name=u'Товары', blank=True)

    objects = CouponManager()

    class Meta:
        verbose_name = u'промо-код'
        verbose_name_plural = u'промо-коды'

    def __unicode__(self):
        return self.code
