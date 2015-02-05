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

        self.wholesale(content)

    def cleanup(self):
        ids = list(set(Product.objects.filter(wholesale_legacy_id__isnull=False).values_list('wholesale_legacy_id', flat=True)))
        for id_ in ids:
            if Product.objects.filter(wholesale_legacy_id=id_).count() == 1:
                continue
            print id_

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

    def _product(self, item):
        try:
            product = Product.objects.get(wholesale_legacy_id=int(item['id']), is_visible=True)
        except Product.DoesNotExist:
            product = Product()
        except Product.MultipleObjectsReturned:
            print item['id']
            for p in Product.objects.filter(wholesale_legacy_id=int(item['id'])):
                print p.id, p.title, p.code, p.sku
            print '-----'
            raise

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
        product.wholesale_legacy_id = item['id']
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

    def wholesale(self, content):
        """Опт"""

        for item in content:
            product = self._product(item)
            if product is None:
                continue

            product.wholesale_price = float(item['unitcost'].replace(',', '.'))
            product.franchisee_price = float(item['frprice'].replace(',', '.'))
            product.pack_amount = int(item['perpack'])

            product.save()
            self._images(product, item)
            self._categories(product, item)
