# -*- coding: utf-8 -*-

from django.conf.urls import patterns

from products.sitemaps import CategorySitemap, ProductSitemap
from pages.sitemaps import PageSitemap
from ideas.sitemaps import IdeaSitemap, IdeaCategorySitemap


SITEMAPS = {
    'categories': CategorySitemap,
    'products': ProductSitemap,
    'pages': PageSitemap,
    'ideas': IdeaSitemap,
    'ideas_categories': IdeaCategorySitemap,
}


urlpatterns = patterns('',
    ('^sitemap/$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': SITEMAPS}),
)
