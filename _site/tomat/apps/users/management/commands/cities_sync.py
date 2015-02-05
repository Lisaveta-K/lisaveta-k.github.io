# -*- coding: utf-8 -*-

import requests
from django.core.management import BaseCommand

from users.models import Country, Region, City


class Command(BaseCommand):

    def handle(self, *args, **options):
        self._countries()
        self._regions()
        self._cities()

    def _countries(self):
        result = requests.get('https://api.vk.com/method/database.getCountries', params={
            'need_full': 1,
            'code': 'RU,UA',
        }).json()['response']

        for item in result:
            try:
                country = Country.objects.get(id=int(item['cid']))
            except Country.DoesNotExist:
                country = Country(id=int(item['cid']), title=item['title'])
                country.save()

    def _regions(self):
        for country in Country.objects.all():
            result = requests.get('https://api.vk.com/method/database.getRegions', params={
                'country_id': country.id,
                'count': 1000,
            }).json()['response']

            for item in result:
                try:
                    region = Region.objects.get(id=int(item['region_id']))
                except Region.DoesNotExist:
                    region = Region(id=int(item['region_id']), title=item['title'], country=country)
                    region.save()

    def _cities(self):
        for region in Region.objects.all():
            result = requests.get('https://api.vk.com/method/database.getCities', params={
                'country_id': region.country_id,
                'region_id': region.id,
                'need_all': 1,
                'count': 1000,
            }).json()['response']

            for item in result:
                try:
                    city = City.objects.get(id=int(item['cid']))
                except City.DoesNotExist:
                    city = City(id=int(item['cid']), region=region, title=item['title'])
                    city.save()
