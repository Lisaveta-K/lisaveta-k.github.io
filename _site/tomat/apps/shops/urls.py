# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('shops.views',
    url(r'^$', 'index', name='shops.index'),
    url(r'^(?P<city_slug>\w+)/$', 'read', name='shops.read'),
)
