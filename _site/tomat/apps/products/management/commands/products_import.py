# -*- coding: utf-8 -*-

import re
import json
import datetime

import pytz
import requests
from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from products.models import Product, Photo, Category


PICTURE_URL = 'http://tomat-podarky.ru/pic/%s/%s.jpg'

SIZE2_RE = re.compile(r'(\d+)\*(\d+)')
SIZE_RE = re.compile(r'(\d+)\*(\d+)\*(\d+)')
TIMEZONE = pytz.timezone('Asia/Irkutsk')


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = args[0]

        if path.startswith('http'):
            content = requests.get(path).json()
        else:
            content = json.load(open(path))

        self.retail(content)

    def _images(self, product, item):
        for idx, pic in enumerate(item['pics']):
            try:
                Photo.objects.get(product=product, legacy_hash=pic['md5'])
            except Photo.DoesNotExist:
                url = PICTURE_URL % (pic['md5'], pic['md5'])
                fp = ContentFile(requests.get(url).content)
                photo = Photo(product=product)
                photo.is_main = idx == 0
                photo.legacy_hash = pic['md5']
                photo.save()
                photo.image.save(pic['filename'], fp)

    def _categories(self, product, item):
        for node in item['node_list']:
            for category in Category.objects.filter(legacy_id__icontains=node['id']):
                ids = category.legacy_id.split(',')
                for id_ in ids:
                    if int(node['id']) == int(id_):
                        product.categories.add(category)
                        break

    def _product(self, item):
        try:
            product = Product.objects.get(id=int(item['id']))
        except Product.DoesNotExist:
            product = Product(id=int(item['id']))

        quantity = int(item.get('qtyi', 0))
        if quantity < 0:
            quantity = 0

        weight = int(item.get('weight', 0))
        if weight < 0:
            weight = 0

        product.sku = item['article']
        product.weight = weight
        product.quantity = quantity
        product.code = item['link']
        product.title = item['name']
        product.description = item['descr']
        product.is_visible = bool(int(item['pub']))
        product.is_wholesale = False
        product.created = TIMEZONE.localize(datetime.datetime.fromtimestamp(int(item['dt'])))

        size = None
        try:
            size = SIZE_RE.findall(u' '.join([item['name'], item.get('alt', ''), item['descr']]))[0]
        except IndexError:
            try:
                size = SIZE2_RE.findall(u' '.join([item['name'], item.get('alt', ''), item['descr']]))[0]
            except IndexError:
                pass

        if size:
            product.size = u'×'.join([str(x) for x in size])

        return product

    def retail(self, content):
        """Розница"""

        for item in content:
            product = self._product(item)

            oldprice = float(item['oldprice'])
            price = float(item['price'])

            if oldprice:
                product.price = oldprice
                product.discount = price
                if product.discount == product.price:
                    product.discount = None
            else:
                product.price = price

            product.save()
            self._images(product, item)
            self._categories(product, item)
