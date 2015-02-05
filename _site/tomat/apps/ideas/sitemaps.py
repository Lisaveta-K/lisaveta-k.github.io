# -*- coding: utf-8 -*-

from django.contrib.sitemaps import Sitemap

from ideas.models import Idea, Category


class IdeaCategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.1

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return Idea.objects.all().order_by('-updated').values_list('updated')[0][0]


class IdeaSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Idea.objects.filter(is_visible=True)

    def lastmod(self, obj):
        return obj.updated
