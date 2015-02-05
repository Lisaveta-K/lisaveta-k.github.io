# -*- coding: utf-8 -*-

from django.db.models.fields import CharField
from django.core.validators import RegexValidator


class DimensionsValidator(RegexValidator):

    def __init__(self):
        super(DimensionsValidator, self).__init__(u'(\d+)x(\d+)x(\d+)')


class DimensionsField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super(DimensionsField, self).__init__(*args, **kwargs)

