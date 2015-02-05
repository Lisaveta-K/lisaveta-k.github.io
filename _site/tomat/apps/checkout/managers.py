# -*- coding: utf-8 -*-

from satchless.process import ProcessManager

from cart.models import Cart
from checkout.steps.auth import AuthStep
from checkout.steps.delivery import DeliveryStep
from checkout.steps.address import AddressStep
from checkout.steps.receipt import ReceiptStep
from checkout.steps.payment import PaymentStep
from checkout.steps.summary import SummaryStep
from checkout.steps.wholesale import WholesaleStep
from checkout.steps.phone import PhoneStep
from users.models import User


class Storage(dict):

    SESSION_KEY = 'checkout'

    modified = False

    def __init__(self, *args, **kwargs):
        super(Storage, self).__init__(*args, **kwargs)

        self.update({
            'address': None,  # id адреса пользователя
            'delivery': None,  # id типа доставки
            'shop': None,  # id магазина, если доставка - самовывоз
            'is_payed': False,
        })

    def clean(self, request):
        del request.session[self.SESSION_KEY]
        del request.session[Cart.SESSION_KEY]


class Checkout(ProcessManager):

    def __init__(self, request):
        self.request = request

        try:
            self.storage = request.session[Storage.SESSION_KEY]
        except KeyError:
            self.storage = Storage()

        if request.user.is_anonymous() or request.user.status in (User.STATUS_CUSTOMER, User.STATUS_ADMIN):
            self.steps = (
                AuthStep(self, request),
                PhoneStep(self, request),
                DeliveryStep(self, request),
                AddressStep(self, request),
                SummaryStep(self, request),
                PaymentStep(self, request),
                ReceiptStep(self, request),
            )
        else:
            self.steps = (
                AuthStep(self, request),
                PhoneStep(self, request),
                WholesaleStep(self, request),
                SummaryStep(self, request),
                ReceiptStep(self, request),
            )

    def save(self):
        self.request.session[Storage.SESSION_KEY] = self.storage

    def __iter__(self):
        return iter(self.steps)
