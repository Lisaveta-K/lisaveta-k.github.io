# -*- coding: utf-8 -*-

import datetime

from django.contrib.sitemaps import Sitemap
from django.db import connection

from products.models import Category, Product


class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        cursor = connection.cursor()
        cursor.execute('''SELECT DISTINCT pc.id
            FROM products_categories AS pc
            RIGHT JOIN products_items_categories AS pic ON pc.id = pic.category_id
            WHERE pc.is_visible = true
        ''')
        ids = [x[0] for x in cursor.fetchall()]

        return Category.objects.filter(id__in=ids)

    def lastmod(self, obj):
        try:
            return obj.products.filter(is_visible=True).order_by('-updated').values_list('updated')[0][0]
        except IndexError:
            return datetime.datetime.now()


class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1.0

    def items(self):
        cursor = connection.cursor()
        cursor.execute('''SELECT DISTINCT pi.id
            FROM products_items AS pi
            RIGHT JOIN products_items_categories AS pic ON pi.id = pic.product_id
            WHERE pi.is_visible = true
        ''')
        ids = [x[0] for x in cursor.fetchall()]

        return Product.objects.filter(id__in=ids, price__gt=0, is_retail=True, quantity__gt=0)

    def lastmod(self, obj):
        return obj.updated
