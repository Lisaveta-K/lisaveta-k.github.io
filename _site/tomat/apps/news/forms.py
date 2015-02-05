# -*- coding: utf-8 -*-

from django import forms

from news.models import News
from utils.forms.widgets import RedactorWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(label=u'Содержание', widget=RedactorWidget)

    class Meta:
        model = News
