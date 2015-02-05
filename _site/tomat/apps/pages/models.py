# -*- coding: utf-8 -*-

import datetime

from django.db import models


class Page(models.Model):
    """Текстовая страница"""

    url = models.CharField(u'Ссылка', max_length=100, db_index=True)
    title = models.CharField(u'Заголовок', max_length=255)
    content = models.TextField(u'Содержание')
    updated = models.DateTimeField(u'Дата последнего обновления', auto_now=True, auto_now_add=True,
        editable=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = u'страница'
        verbose_name_plural = u'страницы'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url

    def get_children(self):
        return Page.objects.filter(url__istartswith=self.url).exclude(url=self.url)
