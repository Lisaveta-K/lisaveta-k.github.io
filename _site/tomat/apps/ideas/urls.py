# -*- coding: utf-8 -*-

from django.conf.urls import url, patterns


urlpatterns = patterns('ideas.views',
    url(r'^$', 'index', name='ideas.index'),
    url(r'^(?P<category_slug>[\w-]+)/$', 'category', name='ideas.category'),
    url(r'^(?P<category_slug>[\w-]+)/(?P<idea_id>\d+)-(.*)/$', 'read', name='ideas.read'),
)
