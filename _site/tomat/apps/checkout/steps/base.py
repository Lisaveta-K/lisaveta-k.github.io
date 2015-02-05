# -*- coding: utf-8 -*-

"""Базовый класс для всех шагов оформления заказа"""

from django.shortcuts import render
from django.db import models
from satchless.process import Step as BaseStep, InvalidData


class Step(BaseStep):
    template = ''

    def __init__(self, checkout, request):
        self.checkout = checkout
        self.request = request
        self.forms = {}

    def __unicode__(self):
        raise NotImplementedError()

    def __nonzero__(self):
        try:
            self.validate()
        except InvalidData:
            return False
        return True

    def save(self):
        raise NotImplementedError()

    def forms_are_valid(self):
        for form in self.forms.values():
            if not form.empty_permitted and not form.is_valid():
                return False

        return True

    def validate(self):
        if not self.forms_are_valid():
            raise InvalidData()

    def process(self, extra_context=None):
        context = extra_context or {}

        if not self.forms_are_valid() or self.request.method == 'GET':
            context['step'] = self

            return render(self.request, self.template, context)

        return self.save()

    @models.permalink
    def get_absolute_url(self):
        return 'checkout.step', (str(self), ), {}

    def add_to_order(self, order):
        raise NotImplementedError()
