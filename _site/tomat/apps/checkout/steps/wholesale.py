# -*- coding: utf-8 -*-

from checkout.steps.base import Step
from checkout.forms import WholesaleCheckoutForm


class WholesaleStep(Step):
    template = 'checkout/steps/wholesale.html'

    def __str__(self):
        return 'wholesale'

    def __init__(self, *args, **kwargs):
        super(WholesaleStep, self).__init__(*args, **kwargs)

        form = WholesaleCheckoutForm(self.request.POST or None)

        self.forms['form'] = form

    def process(self, *args, **kwargs):
        extra = {
            'form': self.forms['form'],
        }

        return super(WholesaleStep, self).process(extra)

    def validate(self):
        if self.checkout.storage.get('delivery'):
            return True

        return super(WholesaleStep, self).validate()

    def save(self):
        data = self.forms['form'].cleaned_data
        self.checkout.storage['delivery'] = data['delivery'].id
        self.checkout.storage['comment'] = data['comment']
        self.checkout.storage['payment'] = data['payment']
        self.checkout.save()
