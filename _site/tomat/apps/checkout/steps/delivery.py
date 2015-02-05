# -* -coding: utf-8 -*-

"""Шаг 3. Тип доставки"""

from checkout.steps.base import Step

from checkout.forms import DeliveryForm
from shops.models import Delivery, Shop


class DeliveryStep(Step):
    template = 'checkout/steps/delivery.html'

    def __str__(self):
        return 'delivery'

    def __init__(self, *args, **kwargs):
        super(DeliveryStep, self).__init__(*args, **kwargs)

        delivery = self.checkout.storage.get('delivery')
        initial = {}
        if delivery:
            initial['type'] = Delivery.objects.get(id=delivery).id

        self.forms['delivery'] = DeliveryForm(self.request.POST or None, initial=initial)

    def process(self, *args, **kwargs):
        extra = {
            'form': self.forms['delivery'],
            'shops': Shop.objects.filter(city__slug='irkutsk', allow_delivery=True),
            'delivery': {
                'pickup': Delivery.objects.get(id=1),
                'mail': Delivery.objects.get(id=2),
                'ems': Delivery.objects.get(id=3),
                'courier': Delivery.objects.get(id=4),
            }
        }

        return super(DeliveryStep, self).process(extra)

    def validate(self):
        order_id = self.checkout.storage.get('order_id')
        if order_id:
            # К моменту создания заказа доставка уже должна быть выбрана
            # либо отсутствовать, если это оптовый или франшизовый заказ
            return True

        if self.checkout.storage.get('delivery') and not 'type' in self.request.POST:
            return True

        return super(DeliveryStep, self).validate()

    def save(self):
        delivery = self.forms['delivery'].cleaned_data['type']
        self.checkout.storage['delivery'] = delivery.id
        if delivery.id == 1:
            shop = self.forms['delivery'].cleaned_data['shop']
            self.checkout.storage['shop'] = shop.id

        self.checkout.save()
