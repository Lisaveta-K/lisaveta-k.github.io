# -*- coding: utf-8 -*-

from satchless.cart import Cart as BaseCart, CartLine as BaseCartLine


class CartLine(BaseCartLine):

    def get_quantity(self, **kwargs):
        return self.quantity


class Cart(BaseCart):

    SESSION_KEY = 'cart'
    COUPON_KEY = 'cart-coupon'

    def create_line(self, product, quantity, data):
        return CartLine(product, quantity, data=data)

    def quantity(self, item, **kwargs):
        for line in self._state:
            if item.id == line.product.id:
                return line.quantity

    def price(self, item, request):
        for line in self._state:
            if item == line.product:
                return line.get_total(request=request).net

    def remove(self, item):
        for line in self._state:
            if item == line.product:
                self.add(item, quantity=0, replace=True)
                return

    def check_constistency(self, user):
        for line in self._state:
            if not line.product.available_for_user(user):
                self.remove(line.product)
