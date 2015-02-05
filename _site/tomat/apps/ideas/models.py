# -*- coding: utf-8 -*-

import uuid
import os.path
import datetime

from django.db import models
from pytils.translit import slugify

from products.models import Product


class Category(models.Model):
    """Категории идей подарков"""

    title = models.CharField(u'Название', max_length=255)
    slug = models.SlugField(u'Алиас', help_text=u'Используется в ссылках')

    class Meta:
        db_table = 'ideas_categories'
        verbose_name = u'категория'
        verbose_name_plural = u'категории'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'ideas.category', (self.slug, ), {}


def idea_image_upload_to(instance, filename):
    today = datetime.date.today()

    return 'ideas/%(year)s/%(month)s/%(name)s%(ext)s' % {
        'year': today.year,
        'month': today.month,
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1],
    }


class Idea(models.Model):
    """Идеи подарков"""

    category = models.ForeignKey(Category, verbose_name=u'Категория')
    title = models.CharField(u'Название', max_length=255)
    content = models.TextField(u'Содержание')
    image = models.ImageField(u'Большое изображение', upload_to=idea_image_upload_to,
        help_text=u'730×300 пикселей')
    thumbnail = models.ImageField(u'Уменьшенное изображение', upload_to=idea_image_upload_to,
        help_text=u'345×230 пикселей')
    is_visible = models.BooleanField(u'Публикуется', default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now_add=True, auto_now=True, default=datetime.datetime.now,
        editable=True)

    products = models.ManyToManyField(Product, related_name='ideas')

    class Meta:
        db_table = 'ideas_idea'
        verbose_name = u'идеи подарков'
        verbose_name_plural = u'идеи подарков'

    def __unicode__(self):
        return self.title

    @property
    def slug(self):
        return slugify(self.title)

    @models.permalink
    def get_absolute_url(self):
        return 'ideas.read', (self.category.slug, self.id, self.slug), {}
