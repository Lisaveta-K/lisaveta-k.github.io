# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.core.management import BaseCommand

from products.models import Product, Photo


class Command(BaseCommand):

    def handle(self, *args, **options):
        for product in Product.objects.all():
            photos = {}
            for photo in product.photos.all():
                if not photo.image:
                    photo.delete()
                    continue

                size = os.stat(photo.image.path).st_size
                if size in photos:
                    old = Photo.objects.get(id=photos[size])
                    if old.id < photo.id:
                        photo.delete()
                    else:
                        old.delete()
                    print 'collision', photos[size], photo.id
                else:
                    photos[size] = photo.id
