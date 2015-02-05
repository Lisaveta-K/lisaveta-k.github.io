# -*- coding: utf-8 -*-

import uuid
import datetime
import os.path

from django.db import models

from users.models import User


class Feedback(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.EmailField(u'E-mail', null=True, blank=True,
        help_text=u'Мы отправим вам ответ на этот адрес')
    title = models.CharField(u'Ваше имя', max_length=255, null=True, blank=True)
    content = models.TextField(u'Вопрос')
    created = models.DateTimeField(u'Дата создания', default=datetime.datetime.now)

    class Meta:
        verbose_name = u'отзыв'
        verbose_name_plural = u'отзывы'

    def __unicode__(self):
        return self.title


def photo_upload_to(instance, filename):
    return 'home/links/%(name)s%(ext)s' % {
        'name': uuid.uuid4().hex,
        'ext': os.path.splitext(filename)[1].lower(),
    }

class Link(models.Model):
    """Ссылка на главной странице"""

    title = models.CharField(u'Текст', max_length=255)
    url = models.URLField(u'Ссылка', help_text=u'На которую будет вести текст/картинка')
    image = models.ImageField(u'Изображение', upload_to=photo_upload_to, blank=True, null=True,
        help_text=u'Желательные размеры: 320×46 пикселей. Если не загружена, выводится текст из поля «Текст»')
    position = models.PositiveSmallIntegerField(u'Позиция', default=0)

    class Meta:
        verbose_name = u'ссылка на главной'
        verbose_name_plural = u'ссылки на главной'

    def __unicode__(self):
        return self.title
