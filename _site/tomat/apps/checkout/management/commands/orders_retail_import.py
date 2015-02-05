# -*- coding: utf-8 -*-

import json
import datetime
import pytz

import requests
from django.core.management import BaseCommand

from users.models import User
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
            try:
                order = Order.objects.get(id=int(item['id']))
            except Order.DoesNotExist:
                order = Order(id=int(item['id']))

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

            for pitem in item.get('lst', ()):
                product = Product.objects.get(id=int(pitem['item_id']))

                try:
                    order_item = OrderItem.objects.get(order=order, product=product)
                except OrderItem.DoesNotExist:
                    order_item = OrderItem(order=order, product=product)
                order_item.amount = int(pitem['qty'])
                order_item.per_item = float(pitem['price'])
                order_item.save()
