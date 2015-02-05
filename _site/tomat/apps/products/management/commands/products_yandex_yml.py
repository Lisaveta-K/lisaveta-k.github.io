# -*- coding: utf-8 -*-

import re
import cgi
import datetime
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.core.management import BaseCommand
from django.utils.html import strip_tags, strip_spaces_between_tags
from django.utils.text import Truncator

from products.models import Product, Photo, Category
from utils.templatetags.text import typograph

WHITESPACE_RE = re.compile('\s+')


def _(text):
    return cgi.escape(text.encode('utf-8'), quote=True)


class Command(BaseCommand):

    def handle(self, *args, **options):
        # Почему генерация XML сделана строками, а не через DOM дерево или другие штуки:
        # на хостинге очень мало памяти, поэтому приходится сильно экономить, чтобы собрать этот файл

        doc = open(args[0], 'w')
        doc.write('''<?xml version="1.0" encoding="utf-8"?><!DOCTYPE yml_catalog SYSTEM "shops.dtd">''')
        doc.write(datetime.datetime.now().strftime('<yml_catalog date="%Y-%m-%d %H:%M">'))

        self.shop(doc)

        doc.write('</yml_catalog>')
        doc.flush()
        doc.close()

    @staticmethod
    def shop(doc):
        doc.write('<shop>')
        doc.write('<name>Томат</name>')
        doc.write('<company>Сеть магазинов подарков</company>')
        doc.write('<url>http://tomat-podarky.ru/</url>')
        doc.write('<currencies><currency id="RUR" rate="1"/></currencies>')

        categories = Command.categories(doc)
        Command.offers(doc, categories)

        doc.write('</shop>')

    @staticmethod
    def categories(doc):
        allowed_categories = []

        queryset = Category.objects.filter(is_visible=True, parent__isnull=True).values_list('id', 'title')
        doc.write('<categories>')
        for id, title in queryset:
            allowed_categories.append(id)
            doc.write('<category id="{}">'.format(id))
            doc.write(_(title))
            doc.write('</category>\n')

            for child_id, child_title in Category.objects.filter(is_visible=True, parent_id=id).values_list('id', 'title'):
                allowed_categories.append(child_id)
                doc.write('<category id="{}" parentId="{}">'.format(child_id, id))
                doc.write(_(child_title))
                doc.write('</category>\n')

        doc.write('</categories>\n')

        return allowed_categories

    @staticmethod
    def offers(doc, categories):
        queryset = Product.objects.filter(is_visible=True, is_retail=True, quantity__gt=0, price__gt=0)
        doc.write('<offers>')
        for product in queryset:
            try:
                category_id = product.categories.filter(parent__isnull=False, id__in=categories).values_list('id', flat=True)[0]
            except IndexError:
                try:
                    category_id = product.categories.filter(parent__isnull=True, id__in=categories).values_list('id', flat=True)[0]
                except IndexError:
                    continue

            text = product.description.strip()
            if text:
                text = strip_tags(strip_spaces_between_tags(product.description)).strip()
                text = typograph(WHITESPACE_RE.sub(' ', text))
                truncator = Truncator(text)
                text = truncator.chars(512)

            doc.write('<offer>')
            doc.write('<url>http://tomat-podarky.ru{}</url>'.format(product.get_absolute_url()))
            doc.write('<price>{}</price>'.format(product.price))
            doc.write('<currencyId>RUR</currencyId>')
            doc.write('<categoryId>{}</categoryId>'.format(category_id))
            doc.write('<delivery>true</delivery>')
            doc.write('<name>')
            doc.write(_(typograph(product.title)))
            doc.write('</name>')
            if text:
                doc.write('<description>')
                doc.write(_(text))
                doc.write('</description>')
            doc.write('</offer>\n')
        doc.write('</offers>')