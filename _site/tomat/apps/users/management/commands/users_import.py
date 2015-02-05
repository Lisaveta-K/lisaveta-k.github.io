# -*- coding: utf-8 -*-

import json
import urllib2
import datetime

from django.core.management import BaseCommand

from users.models import User, Address, Company, City


HASH_STRING = 'md5$1$$%s'


CITY_MAPPINGS = {
    u'Иркутск': 57,
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = args[0]

        if path.startswith('http'):
            content = json.load(urllib2.urlopen(path))
        else:
            content = json.load(open(path))

        for item in content:
            if not '@' in item['username']:
                print item['username']
                continue

            try:
                user = User.objects.get(id=int(item['id']))
            except User.DoesNotExist:
                user = User(id=int(item['id']))

            user.email = item['username']
            user.password = item['password']
            user.title = item['fullname']
            user.phone = item.get('phone', '')

            birthday = None
            if 'year' in item:
                birthday = datetime.date(int(item['year']), int(item['month']), int(item['mday']))
            user.birthday = birthday

            user.is_active = item['status'] == '1'

            if item['franch'] == '10':
                user.status = User.STATUS_FRANCHISEE
            elif item['retail'] == '10':
                user.status = User.STATUS_CUSTOMER
            elif item['retail'] == '0':
                user.status = User.STATUS_WHOLESALE

            user.save()

            for addr in item['addresses']:
                try:
                    address = Address.objects.get(id=int(addr['id']))
                except Address.DoesNotExist:
                    address = Address(id=int(addr['id']))

                address.user = user
                if not address.city:
                    address.city = addr['city']
                if not address.postal_code:
                    address.postal_code = ''
                if not address.street:
                    address.street = ''
                if not address.house:
                    address.house = ''
                if not address.flat:
                    address.flat = ''
                if not address.phone:
                    address.phone = addr.get('to_phone', addr.get('fax', ''))
                if not address.email:
                    address.email = addr.get('to_email', '')
                address.receiver_title = addr.get('to_name', addr.get('name', ''))
                address.original_string = addr['address']

                address.save()
            '''
            if 'company_name' in item:
                try:
                    company = Company.objects.get(user=user)
                except Company.DoesNotExist:
                    company = Company(user=user)

                company.title = item['company_name']
                if item['company_city'] in CITY_MAPPINGS:
                    city = City.objects.get(id=CITY_MAPPINGS[item['company_city']])
                else:
                    city = City.objects.get(title__iexact=item['company_city'])
                company.city = city
                company.phone = item['company_fax']
                company.industry = item['company_industry']
                company.save()
            '''
