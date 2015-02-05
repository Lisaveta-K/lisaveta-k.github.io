# -*- coding: utf-8 -*-

import json
import datetime
import pytz

import requests
from django.core.management import BaseCommand

from users.models import User, Company
from checkout.models import Order, OrderItem
from products.models import Product
from shops.models import Delivery

STATUSES_MAPPING = {
    '0': 0,
    '50': 1,
    '70': 2,
    '100': 3,
    '200': 4,
    '500': 5,
}

PAYMENT_MAPPING = {
    'robo': 0,
    'cashpick': 1,
    'courier': 2,
}

DELIVERY_MAPPINGS = {
    'self': 1,
    'russianpost': 2,
    'expresspost': 3,
    'courier': 4,
}

TIMEZONE = pytz.timezone('Asia/Irkutsk')


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = args[0]

        if path.startswith('http'):
            content = requests.get(path).json()
        else:
            content = json.load(open(path))

        for item in content:
            id_ = int(item['id']) + 300  # 260 розничных заказов, плюс небольшой отступ
            try:
                order = Order.objects.get(id=id_)
            except Order.DoesNotExist:
                order = Order(id=id_)

            print 'Processing order %s' % item['id']

            order.code = item['code']
            order.net = float(item['amt'])
            order.comment = item.get('comment', '')
            order.created = TIMEZONE.localize(datetime.datetime.fromtimestamp(int(item['cdt'])))
            order.status = STATUSES_MAPPING[item['status']]
            order.payment_type = PAYMENT_MAPPING.get(item.get('payment'))
            order.delivery_cost = int(item.get('dcost', 0))

            try:
                order.delivery = Delivery.objects.get(id=DELIVERY_MAPPINGS.get(item.get('delivery')))
            except Delivery.DoesNotExist:
                pass

            try:
                order.user = User.objects.get(id=int(item['user_id']))
            except User.DoesNotExist:
                try:
                    if not 'email' in item:
                        raise User.DoesNotExist()
                    order.user = User.objects.get(email=item['email'])
                except User.DoesNotExist:
                    pass

            order.save()

            if order.user:
                try:
                    company = Company.objects.get(user=order.user)
                except Company.DoesNotExist:
                    company = Company(user=order.user)

                company.title = item.get('addr_name') or item.get('company_name', '')
                company.city = item.get('company_city', '')
                company.director = item.get('director', '')
                company.juridical_address = item.get('jaddress', '')
                company.post_address = item.get('address', '')
                company.industry = item.get('company_industry', '')
                company.phone = item.get('phone', '')
                company.inn = item.get('inn', '')
                company.ogrn = item.get('ogrn', '')
                company.save()
            else:
                print 'Order %d cant be linked to user' % order.id

            for pitem in item.get('lst', ()):
                product_id = int(pitem['item_id'])
                try:
                    product = Product.objects.get(wholesale_legacy_id=product_id, is_visible=True)
                    kwargs = {
                        'product': product,
                    }
                except Product.DoesNotExist:
                    print 'Unknown product with id %s' % pitem['item_id']
                    kwargs = {
                        'product_legacy_id': product_id,
                    }
                except Product.MultipleObjectsReturned:
                    print product_id
                    raise

                try:
                    order_item = OrderItem.objects.get(order=order, **kwargs)
                except OrderItem.DoesNotExist:
                    order_item = OrderItem(order=order, **kwargs)
                order_item.product_legacy_id = product_id
                order_item.amount = int(pitem['qty'])
                order_item.per_item = float(pitem['price'])
                order_item.save()
