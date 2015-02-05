# -* -coding: utf-8 -*-

"""Если у пользователя в профиле не указан телефон, уточняем его"""

from satchless.process import InvalidData

from checkout.steps.base import Step
from checkout.forms import PhoneForm


class PhoneStep(Step):
    template = 'checkout/steps/phone.html'

    def __str__(self):
        return 'phone'

    def __init__(self, *args, **kwargs):
        super(PhoneStep, self).__init__(*args, **kwargs)

        number = self.request.POST.get('number', '') or (self.request.user.phone if self.request.user.is_authenticated() else '')

        initial = {
            'number': number,
        }

        self.forms['phone'] = PhoneForm(self.request.POST or None, initial=initial)

    def process(self, *args, **kwargs):
        extra = {
            'form': self.forms['phone'],
        }

        return super(PhoneStep, self).process(extra)

    def validate(self):
        if self.request.user.phone:
            return True

        raise InvalidData()

    def save(self):
        number = self.forms['phone'].cleaned_data['number']
        self.request.user.phone = number
        self.request.user.save()
