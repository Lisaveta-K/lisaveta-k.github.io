# -*- coding: utf-8 -*-

import os
import uuid

from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from pytils.translit import slugify


class City(models.Model):
    title = models.CharField(u'Название', max_length=255)
    slug = models.SlugField(u'Алиас')

    class Meta:
        db_table = 'shops_cities'
        verbose_name = u'Город'
        verbose_name_plural = u'Города'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'shops.views.read', (self.slug, ), {}


def shop_mart_upload_to(instance, filename):
    return 'shops/mart/%(name)s%(ext)s' % {
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1].lower(),
    }


class Shop(models.Model):
    """Магазин в городе"""

    city = models.ForeignKey(City, related_name='shops', verbose_name=u'Город')
    title = models.CharField(u'Название', max_length=255)
    description = models.TextField(u'Описание', blank=True)
    address = models.CharField(u'Адрес', max_length=255)
    phones = models.CharField(u'Телефон', max_length=255)
    worktime = models.CharField(u'Время работы', max_length=255)
    point = models.PointField()
    mart = models.ImageField(upload_to=shop_mart_upload_to, null=True, blank=True, verbose_name=u'Логотип ТЦ')
    position = models.PositiveSmallIntegerField(u'Позиция', default=0)
    allow_delivery = models.BooleanField(u'Можно заказать доставку', default=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name = u'магазин'
        verbose_name_plural = u'магазины'

    def __unicode__(self):
        return self.title


def category_cover_upload_to(instance, filename):
    return 'shops/delivery/%(name)s%(ext)s' % {
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1].lower(),
    }


class Delivery(models.Model):
    TYPE_SELF = 1  # Самовывоз
    TYPE_RUSSIANPOST = 2
    TYPE_EXPRESSPOST = 3
    TYPE_COURIER = 4
    TYPE_TRANSPORT = 5
    TYPE_WHOLESALE_SELF = 6
    TYPE_IRKUTSK_DELIVERY = 7

    COSTS = {
        TYPE_SELF: 0,
        TYPE_RUSSIANPOST: 300,
        TYPE_EXPRESSPOST: 600,
        TYPE_COURIER: 100,
        TYPE_TRANSPORT: 0,
        TYPE_WHOLESALE_SELF: 0,
        TYPE_IRKUTSK_DELIVERY: 0,
    }

    title = models.CharField(u'Название', max_length=255)
    caption = models.TextField(u'Короткое описание', help_text=u'Выводится на странице товара')
    content = models.TextField(u'Полное описание')
    image = models.ImageField(u'Изображение', upload_to=category_cover_upload_to)
    position = models.PositiveSmallIntegerField(u'Позиция', default=0)
    is_retail = models.BooleanField(u'Доступна розничным покупателям', default=False, db_index=True)
    is_wholesale = models.BooleanField(u'Доставка оптовикам', default=False, db_index=True)

    class Meta:
        verbose_name = u'доставка'
        verbose_name_plural = u'доставка'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        url = reverse('home.views.delivery')

        return '%s#%s' % (url, self.slug)

    def is_requiring_instant_payment(self):
        return self.id in (self.TYPE_RUSSIANPOST, self.TYPE_RUSSIANPOST)

    def have_payment_choices(self):
        return self.id in (self.TYPE_COURIER, self.TYPE_SELF)

    def is_self_pickup(self):
        return self.id in (self.TYPE_SELF, self.TYPE_WHOLESALE_SELF)

    def cost(self, net=None):
        if net and self.id == self.TYPE_TRANSPORT and net > 10000:
            return 0

        if net and self.id == self.TYPE_RUSSIANPOST and net > 3000:
            return 0

        return self.COSTS.get(self.id, 0)

    @property
    def slug(self):
        return slugify(self.title)


class Discount(models.Model):
    """Скидка по накопительной карте"""

    id = models.PositiveIntegerField(u'Код', primary_key=True)
    title = models.CharField(u'Название', max_length=255)
    percent = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = u'скидка'
        verbose_name_plural = u'скидки'

    def __unicode__(self):
        return u'%d' % self.id

