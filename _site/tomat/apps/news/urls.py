# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('news.views',
    url(r'^$', 'index', name='news.index'),
    url(r'^(?P<object_id>\d+)/$', 'read', name='news.read'),
)
