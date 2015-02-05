# -*- coding: utf-8 -*-

from django import forms

from ideas.models import Idea
from annoying.decorators import autostrip
from utils.forms.widgets import RedactorWidget
from pytils.translit import slugify

from products.fields import ProductSelect2MultipleField


@autostrip
class IdeaAdminForm(forms.ModelForm):
    content = forms.CharField(label=u'Содержание', widget=RedactorWidget)
    products = ProductSelect2MultipleField(label=u'Продукты', required=False)

    class Meta:
        model = Idea
        fields = ('title', 'content', 'image', 'thumbnail', 'is_visible', 'category', 'products')


class CategoryAdminForm(forms.ModelForm):
    slug = forms.SlugField(label=u'Алиас')

    def clean(self):
        title = self.cleaned_data.get('title')
        slug = self.cleaned_data.get('slug')

        if not slug:
            self.cleaned_data['slug'] = slugify(title)

        return self.cleaned_data
