# -*- coding: utf-8 -*-

"""Шаг 2

Адрес доставки"""

import json

from checkout.steps.base import Step
from checkout.models import CourierCity
from users.models import Address
from users.forms import AddressForm, CourierCityAddressForm, DeliveryDateTimeForm


class AddressStep(Step):
    template = 'checkout/steps/address.html'

    def __str__(self):
        return 'address'

    def __init__(self, *args, **kwargs):
        super(AddressStep, self).__init__(*args, **kwargs)

        initial = {}
        if self.request.user.is_authenticated():
            initial.update({
                'email': self.request.user.email,
                'phone': self.request.user.phone,
            })

        form_empty_permitted = False
        if self.checkout.storage.get('address') or self.request.POST.get('address'):
            form_empty_permitted = True
        form_kwargs = {
            'initial': initial,
            'empty_permitted': form_empty_permitted,
        }

        if self.checkout.storage.get('delivery') == 4:
            form_cls = CourierCityAddressForm
        else:
            form_cls = AddressForm

        self.forms['address'] = form_cls(self.request.POST or None, **form_kwargs)
        self.forms['delivery_datetime'] = DeliveryDateTimeForm(self.request.POST or None, empty_permitted=True, auto_id='id_for_%s')
        if 'address' in self.request.POST:
            self.forms['address'] = form_cls(None, **form_kwargs)
        else:
            self.forms['delivery_datetime'] = DeliveryDateTimeForm(None, empty_permitted=True, auto_id='id_for_%s')

    def process(self, *args, **kwargs):
        if self.checkout.storage.get('delivery') == 1:  # самовывоз, магазин уже выбран
            return

        address_id = self.checkout.storage.get('address') or self.request.POST.get('address')
        courier_cities = {}
        for city in CourierCity.objects.all():
            courier_cities[city.id] = city.price

        extra = {
            'addresses': Address.objects.filter(user=self.request.user, is_deleted=False),
            'address_id': int(address_id) if address_id else None,
            'form': self.forms['address'],
            'delivery_form': self.forms['delivery_datetime'],
            'delivery_type': self.checkout.storage.get('delivery'),
            'courier_cities': json.dumps(courier_cities),
        }

        return super(AddressStep, self).process(extra)

    def forms_are_valid(self):
        if self.checkout.storage.get('delivery') == 1:
            print 1
            return True

        if 'address' in self.request.POST:
            print 2
            address = Address.objects.get(id=self.request.POST['address'], user=self.request.user)
            if 'delivery_date' in self.request.POST:
                form = DeliveryDateTimeForm(self.request.POST)
                if not form.is_valid():
                    return False
                else:
                    if 'delivery_date' in form.cleaned_data:
                        self.checkout.storage['delivery_date'] = form.cleaned_data['delivery_date']
                    if 'delivery_time' in form.cleaned_data:
                        self.checkout.storage['delivery_time'] = form.cleaned_data['delivery_time']
            return True

        if self._get_address():
            print 3
            return True
        print 4
        return super(AddressStep, self).forms_are_valid()

    def save(self):
        instance = None
        if not 'address' in self.request.POST:
            form = self.forms['address']

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = self.request.user
                if 'delivery_date' in form.cleaned_data:
                    self.checkout.storage['delivery_date'] = form.cleaned_data['delivery_date']
                if 'delivery_time' in form.cleaned_data:
                    self.checkout.storage['delivery_time'] = form.cleaned_data['delivery_time']
                instance.save()

        else:
            instance = Address.objects.get(user=self.request.user, id=self.request.POST['address'])
        if instance:
            self.checkout.storage['address'] = instance.id
            self.checkout.save()

    def _get_address(self):
        try:
            address_id = int(self.checkout.storage.get('address'))
            return Address.objects.get(user=self.request.user, id=address_id, is_deleted=False)
        except (TypeError, ValueError, Address.DoesNotExist):
            pass
