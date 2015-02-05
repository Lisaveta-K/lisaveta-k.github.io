# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('uploads.views',
    url(r'^image/$', 'upload_image'),
    url(r'^file/$', 'upload_file'),
)
