# -*- coding: utf-8 -*-

"""Шаг 4. Оплата"""

import datetime
import decimal

from django.shortcuts import render
from satchless.process import InvalidData

from checkout.models import Order, OrderItem, CourierCity
from checkout.steps.base import Step
from checkout.forms import PaymentForm
from users.heplers import combine_date_and_time
from users.models import Address
from shops.models import Delivery, Shop
from cart.models import Cart
from adverts.models import Coupon


class SummaryStep(Step):
    template = 'checkout/steps/summary.html'

    def __str__(self):
        return 'summary'

    def process(self, *args, **kwargs):
        coupon = self._get_coupon()
        diff = 0

        if self.request.method == 'GET':

            net = self.request.cart.get_total(request=self.request).net
            if coupon:
                matches = []
                products_ids = list(coupon.products.all().values_list('id', flat=True))
                categories_ids = list(coupon.categories.all().values_list('id', flat=True))

                for item in self.request.cart:
                    if item.product.id in products_ids:
                        matches.append(item)
                        continue

                    for category_id in item.product.categories.all().values_list('id', flat=True):
                        if category_id in categories_ids:
                            matches.append(item)
                            continue

                matches = list(set(matches))

                # Сумма стоимости всех товаров
                amount = sum([x.product.price_for_user(self.request.user) * x.quantity for x in matches])
                if coupon.discount_percent:
                    diff = decimal.Decimal((float(amount) / 100.0) * coupon.discount_percent)
                else:
                    diff = coupon.discount_amount
                net -= diff

            address = self._get_address()

            try:
                delivery = Delivery.objects.get(id=self.checkout.storage['delivery'])
                delivery_cost = delivery.cost(net)
                print 'COST', delivery.id
                if delivery.id == Delivery.TYPE_COURIER:
                    if net > 1000 and (address.city.strip().lower() == u'Иркутск'.lower() or address.courier_city_id == 1):
                        delivery_cost = 0
                    elif address.courier_city_id:
                        delivery_cost = address.courier_city.price

            except Delivery.DoesNotExist:
                delivery = None
                delivery_cost = 0


            extra = {
                'cart': self.request.cart,
                'total': net + diff,
                'address': address,
                'shop': self._get_shop(),
                'delivery': delivery,
                'delivery_date': self._get_delivery_date(),
                'delivery_time': self._get_delivery_time(),
                'net': delivery_cost + net,
                'coupon': coupon,
                'diff': diff,
                'delivery_cost': delivery_cost,
            }

            return render(self.request, self.template, extra)

        return self.save()

    def validate(self):
        is_confirmed = self.checkout.storage.get('is_confirmed', False)
        if not is_confirmed:
            raise InvalidData()

    def save(self):
        self.checkout.storage['is_confirmed'] = True

        order = Order()
        order.user = self.request.user
        order.address = self._get_address()
        order.delivery_date = self._get_delivery_date()
        order.delivery_time = self._get_delivery_time()
        order.shop = self._get_shop()
        order.status = Order.STATUS_RECEIVED
        order.code = '!'

        form = PaymentForm(self.request.POST)
        form.is_valid()
        order.comment = form.cleaned_data.get('comment', self.checkout.storage.get('comment', ''))
        net = self.request.cart.get_total(request=self.request).net

        try:
            order.delivery = Delivery.objects.get(id=self.checkout.storage['delivery'])
        except Delivery.DoesNotExist:
            order.delivery = None
            order.delivery_cost = 0
        else:
            order.delivery_cost = order.delivery.cost(net)
            print 'DELIVERY', order.delivery_id
            if order.delivery_id == Delivery.TYPE_SELF:
                order.payment_type = Order.PAYMENT_CASHPICK

            elif order.delivery_id == Delivery.TYPE_COURIER:
                order.payment_type = Order.PAYMENT_COURIER
                if net > 1000 and (order.address.city == u'Иркутск' or order.address.courier_city_id == 1):  # Иркутск
                    order.delivery_cost = 0
                elif order.address.courier_city:
                    order.delivery_cost = order.address.courier_city.price

            elif order.delivery_id == Delivery.TYPE_RUSSIANPOST:
                order.payment_type = Order.PAYMENT_ROBOKASSA

            elif order.delivery_id == Delivery.TYPE_EXPRESSPOST:
                pass

        order.products_price = self.request.cart.get_total(request=self.request).net
        order.net = self.request.cart.get_total(request=self.request).net + order.delivery_cost
        order.status = Order.STATUS_PAYMENT_WAITING

        order.save()

        for line in self.request.cart:
            item = OrderItem(order=order, product=line.product, amount=line.quantity,
                per_item=line.product.price_for_user(self.request.user) or 0)

            if line.data:
                item.sign = line.data.get('sign')

            item.save()

        coupon = self._get_coupon()
        if coupon:
            diff = self._apply_coupon(order, coupon)
            order.coupon = coupon
            order.net -= diff
            order.save()
            try:
                del self.request.session[Cart.COUPON_KEY]
            except KeyError:
                pass

        self.checkout.storage['order_id'] = order.id
        self.checkout.save()

    def _get_address(self):
        address_id = self.checkout.storage.get('address')
        address = None
        if address_id:
            address = Address.objects.get(id=address_id)

        return address

    def _get_delivery_date(self):
        return self.checkout.storage.get('delivery_date', None)

    def _get_delivery_time(self):
        return self.checkout.storage.get('delivery_time', None)

    def _get_shop(self):
        shop_id = self.checkout.storage.get('shop')
        shop = None
        if shop_id:
            shop = Shop.objects.get(id=shop_id)

        return shop

    def _get_coupon(self):
        coupon = None
        if Cart.COUPON_KEY in self.request.session:
            data = self.request.session[Cart.COUPON_KEY]
            try:
                coupon = Coupon.objects.get(id=data['id'])
                if data['expires'] < datetime.datetime.now():
                    raise Coupon.DoesNotExist()
            except Coupon.DoesNotExist:
                del self.request.session[Cart.COUPON_KEY]

        return coupon

    def _apply_coupon(self, order, coupon):
        matches = []
        products_ids = list(coupon.products.all().values_list('id', flat=True))
        categories_ids = list(coupon.categories.all().values_list('id', flat=True))

        for item in OrderItem.objects.filter(order=order).select_related('product'):
            if item.product_id in products_ids:
                matches.append(item)
                continue

            for category_id in item.product.categories.all().values_list('id', flat=True):
                if category_id in categories_ids:
                    matches.append(item)
                    continue

        matches = list(set(matches))

        # Сумма стоимости всех товаров
        amount = sum([x.net * x.amount for x in matches])

        if coupon.discount_percent:
            return decimal.Decimal((float(amount) / 100.0) * coupon.discount_percent)
        else:
            return coupon.discount_amount
