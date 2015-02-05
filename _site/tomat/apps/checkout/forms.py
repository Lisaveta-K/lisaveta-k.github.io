# -*- coding: utf-8 -*-

from django import forms

from shops.models import Delivery, Shop, Discount
from checkout.models import Order


class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)


class DeliveryForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Delivery.objects.filter(is_retail=True))
    shop = forms.ModelChoiceField(queryset=Shop.objects.filter(city__slug='irkutsk'), required=False)

    def clean(self):
        type_ = self.cleaned_data.get('type')
        shop = self.cleaned_data.get('shop')

        if type_ == 1 and not shop:
            raise forms.ValidationError(u'Магазин должен быть выбран')

        return self.cleaned_data


class PaymentForm(forms.Form):
    """Форма для шага подтверждения заказа"""

    comment = forms.CharField(widget=forms.Textarea, label=u'Комментарий к заказу', required=False)


class DiscountForm(forms.Form):

    number = forms.IntegerField(label=u'Номер карты', required=False, widget=forms.TextInput(attrs={
        'maxlength': 4,
        'class': '',
    }))
    title = forms.CharField(label=u'Фамилия', required=False)

    def clean_number(self):
        value = self.cleaned_data['number']
        if not Discount.objects.filter(id=value).exists():
            raise forms.ValidationError(u'Нет дисконтой карты с таким номером')

        return value

    def clean(self):
        data = self.cleaned_data
        number = data.get('number')
        title = data.get('title', '').strip()

        if any([number, title]) and not all([number, title]):
            raise forms.ValidationError(u'Неправильные данные дисконтной карты')

        if number and title and not Discount.objects.filter(id=number, title__iexact=title).exists():
            raise forms.ValidationError(u'Неизвестная дисконтная карта')

        return data


class WholesaleCheckoutForm(forms.Form):
    WHOLESALE_PAYMENT_CHOICES = (
        (Order.PAYMENT_CASHPICK, u'Наличный расчет'),
        (Order.PAYMENT_CASHLESS, u'Безналичный расчет'),
    )

    delivery = forms.ModelChoiceField(queryset=Delivery.objects.filter(is_wholesale=True).order_by('position'),
        empty_label=None, required=True)
    payment = forms.IntegerField(label=u'Оплата', widget=forms.RadioSelect(choices=WHOLESALE_PAYMENT_CHOICES),
        required=True)
    comment = forms.CharField(label=u'Комментарий к заказу', required=False, widget=forms.Textarea)

    def clean(self):
        delivery = self.cleaned_data.get('delivery')
        payment = self.cleaned_data.get('payment')

        if not delivery:
            raise forms.ValidationError(u'Не выбрана доставка')

        if not payment:
            raise forms.ValidationError(u'Не выбран тип оплаты')

        if delivery.id == Delivery.TYPE_TRANSPORT and payment != Order.PAYMENT_CASHLESS:
            raise forms.ValidationError(u'Доставка транспортной компанией может быть оплачена только безналичным расчетом')

        return self.cleaned_data


class PhoneForm(forms.Form):
    number = forms.CharField(label=u'Номер телефона', max_length=50, required=True)
