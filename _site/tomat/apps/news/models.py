# -*- coding: utf-8 -*-

import uuid
import os.path

from django.db import models


def news_preview_upload_to(instance, filename):
    return 'news/preview/%(name)s%(ext)s' % {
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1].lower(),
    }

class News(models.Model):
    title = models.CharField(u'Название', max_length=255)
    caption = models.TextField(u'Краткое содержание')
    content = models.TextField(u'Содержание')
    date_published = models.DateField(u'Дата публикации')
    preview = models.ImageField(u'Превью', help_text=u'Выводится в списке новостей, 140×100', null=True, blank=True,
        upload_to=news_preview_upload_to)
    is_visible = models.BooleanField(u'Отображается', default=False, db_index=True)

    class Meta:
        verbose_name = u'новость'
        verbose_name_plural = u'новости'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'news.read', (self.id, ), {}
