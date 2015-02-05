# -*- coding: utf-8 -*-

"""Последний шаг"""

from satchless.process import InvalidData

from checkout.steps.base import Step
from cart.models import Cart
from checkout.models import Order, OrderItem
from checkout.helpers import send_order_mails


class ReceiptStep(Step):
    template = 'checkout/steps/receipt.html'

    def __str__(self):
        return 'receipt'

    def forms_are_valid(self):
        # Последний шаг
        return self == self.checkout.get_next_step()

    def add_to_order(self, order):
        self.checkout.storage.clean(self.request)

    def validate(self):
        raise InvalidData()

    def save(self):
        pass

    def process(self, extra_context=None):
        order = Order.objects.get(id=self.checkout.storage['order_id'])
        items = OrderItem.objects.filter(order=order).select_related('product')

        self.checkout.storage.clean(self.request)
        self.request.session[Cart.SESSION_KEY] = Cart()

        if not order.is_emails_sended:
            send_order_mails(order, self.request.user)
            Order.objects.filter(pk=order.pk).update(is_emails_sended=True)

        extra_context = {
            'order': order,
            'items': items,
        }

        response = super(ReceiptStep, self).process(extra_context)

        return response
