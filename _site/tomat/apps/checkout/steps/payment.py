# -*- coding: utf-8 -*-

"""Шаг 4. Оплата"""

import decimal
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.core.urlresolvers import reverse
from satchless.process import InvalidData

from cart.models import Cart
from checkout.models import Order, OrderItem
from checkout.steps.base import Step
from checkout.forms import PaymentForm, DiscountForm
from checkout.helpers import send_order_mails
from robokassa.forms import RobokassaForm
from users.models import Address
from shops.models import Shop, Discount
from adverts.models import Coupon


class PaymentStep(Step):
    template = 'checkout/steps/payment.html'

    def __str__(self):
        return 'payment'

    def process(self, *args, **kwargs):
        order = Order.objects.get(id=self.checkout.storage['order_id'])
        form = PaymentForm()

        if self.request.method == 'POST':
            action = self.request.POST.get('action')

            if action == 'discount':
                discount_form = DiscountForm(self.request.POST)
                if discount_form.is_valid():
                    discount = Discount.objects.get(id=discount_form.cleaned_data['number'],
                        title__iexact=discount_form.cleaned_data['title'])
                    order.discount = discount
                    discount_value = (order.products_price + order.delivery_cost) / 100 * order.discount.percent
                    order.net -= discount_value
                    order.save()

                    return HttpResponseRedirect('.')
            else:
                return self.save()

        else:
            discount_initial = {}
            if order.discount:
                discount_initial = {
                    'number': order.discount.id,
                    'title': order.discount.title,
                }
            discount_form = DiscountForm(initial=discount_initial)

        coupon = self._get_coupon()
        net = self.request.cart.get_total(request=self.request).net

        diff = None
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
            amount = sum([x.product.price_for_user(self.request.user) * x.amount for x in matches])
            if coupon.discount_percent:
                diff = decimal.Decimal((float(amount) / 100.0) * coupon.discount_percent)
            else:
                diff = coupon.discount_amount

        extra = {
            'order': order,
            'cart': self.request.cart,
            'address': self._get_address(),
            'shop': self._get_shop(),
            'delivery': order.delivery,
            'form': form,
            'discount_form': discount_form,
            'total': net,
            'coupon': self._get_coupon(),
            'diff': diff,
        }

        return render(self.request, self.template, extra)


    def validate(self):
        if not 'order_id' in self.checkout.storage:
            raise InvalidData()

        is_payed = self.checkout.storage.get('is_payed', False)
        if not is_payed:
            raise InvalidData()

    def save(self):
        order = Order.objects.get(id=self.checkout.storage['order_id'])

        order.comment = self.request.POST.get('comment', '').strip()

        # Выбор пользователем типа оплаты
        payment_type = self.request.POST.get('payment')
        if payment_type not in ('cash', 'robokassa'):
            payment_type = None

        # Нет доставки - заказ оптового покупателя
        if not order.delivery:
            self.checkout.storage['is_payed'] = True
            order.status = Order.STATUS_PAYMENT_WAITING
            order.is_emails_sended = True
            order.save()
            self.checkout.save()

            send_order_mails(order, self.request.user)
            self.checkout.storage['is_notified'] = True

            return

        # Самовывоз - не нужна оплата
        # Оплата наличкой - не нужна оплата
        elif payment_type == 'cash':
            self.checkout.storage['is_payed'] = True
            order.payment_type = Order.PAYMENT_CASHPICK
            order.status = Order.STATUS_PAYED
            order.is_emails_sended = True
            order.save()
            self.checkout.save()

            send_order_mails(order, self.request.user)
            self.checkout.storage['is_notified'] = True

            return

        order.payment_type = Order.PAYMENT_ROBOKASSA
        order.save()

        form = RobokassaForm(initial={
            'OutSum': order.net,
            'InvId': order.id,
            'Desc': u'Заказ №%s в интернет-магазине «Томат»' % order.id,
            'Email': self.request.user.email,
            'Culture': 'ru',
        })
        if settings.DEBUG:
            form.target = reverse('checkout.views.rk_test_start')
            url = form.get_redirect_url()
        else:
            url = form.get_redirect_url()

        self.checkout.save()

        return HttpResponseRedirect(url)

    def _get_address(self):
        address_id = self.checkout.storage.get('address')
        address = None
        if address_id:
            try:
                address = Address.objects.get(id=address_id, user=self.request.user, is_deleted=False)
            except Address.DoesNotExist:
                address = None

        return address

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
