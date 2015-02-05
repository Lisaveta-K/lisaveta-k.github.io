# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('checkout.views',
    # Robokassa

    url(r'^$', 'step', kwargs={'step': None}, name='checkout.index'),
    url(r'^(?P<step>[a-z0-9-]+)/$', 'step', name='checkout.step')
)
