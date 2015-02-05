# -*- coding: utf-8 -*-

from django.contrib.gis import forms

from shops.models import Shop
from utils.forms.widgets import PointWidget


class ShopAdminForm(forms.ModelForm):
    point = forms.PointField(widget=PointWidget, label=u'Координаты')

    class Meta:
        model = Shop
