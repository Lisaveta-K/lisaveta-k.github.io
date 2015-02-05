# -*- coding: utf-8 -*-

from django import forms

from products.models import Product


class CartUpdateForm(forms.Form):
    quantity = forms.IntegerField(initial=1, widget=forms.TextInput(attrs={'class': 'input-small'}))
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput)
    replace = forms.BooleanField(required=False, initial=True)

    def clean_quantity(self):
        value = self.cleaned_data['quantity']
        if value <= 0:
            raise forms.ValidationError(u'Неправильное число товаров')

        return value


class CartDeleteForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput)


class ProductSignForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput)
    text = forms.CharField(label=u'Подпись', widget=forms.Textarea)
