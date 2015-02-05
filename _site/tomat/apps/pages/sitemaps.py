# -*- coding: utf-8 -*-

import datetime

from django.contrib.sitemaps import Sitemap

from pages.models import Page


class PageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.3

    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        return obj.updated
