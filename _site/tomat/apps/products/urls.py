# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('products.views',
    url(r'^(?P<slug>[\w\-]+)/$', 'categories.parent'),
    url(r'^(?P<parent_slug>[\w\-]+)/(?P<slug>[\w\-]+)/$', 'categories.read'),
    url(r'^(?P<parent_slug>[\w\-]+)/(?P<slug>[\w\-]+)/(?P<product_id>\d+)-(.*?)/$', 'products.read'),
)
