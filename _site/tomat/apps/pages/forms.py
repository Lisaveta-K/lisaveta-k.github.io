# -*- coding: utf-8 -*-

from django import forms
from annoying.decorators import autostrip

from pages.models import Page
from utils.forms.widgets import RedactorWidget


@autostrip
class PageAdminForm(forms.ModelForm):
    content = forms.CharField(label=u'Содержание', widget=RedactorWidget)

    class Meta:
        model = Page

    def clean_url(self):
        url = self.cleaned_data.get('url', '').strip().strip('/')
        url = u'/{0}/'.format(url)

        queryset = Page.objects.filter(url=url)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError(u'Уже есть страница с ссылкой {0}'.format(url))

        return url
