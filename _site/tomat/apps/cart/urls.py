# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('cart.views',
    url(r'^$', 'index', name='cart.index'),
    url(r'^update/$', 'update', name='cart.update'),
    url(r'^delete/$', 'delete', name='cart.delete'),
    url(r'^clear/$', 'clear', name='cart.clear'),
    url(r'^reload/$', 'reload', name='cart.reload'),
    url(r'^status/$', 'status', name='cart.status'),
    url(r'^postcart-sign/$', 'sign', name='cart.sign'),
)
