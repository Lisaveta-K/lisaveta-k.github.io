# -*- coding: utf-8 -*-

from django import forms

from annoying.decorators import autostrip
from mptt.fields import TreeNodeMultipleChoiceField
from PIL import Image

from products.models import Category
from products.fields import CategorySelect2MultipleField, ProductSelect2MultipleField
from adverts.models import Promo, Coupon


@autostrip
class PromoAdminForm(forms.ModelForm):
    """Форма промо-блока для админки"""

    color = forms.CharField(label=u'Цвет фона', max_length=7)
    categories = TreeNodeMultipleChoiceField(queryset=Category.objects.all(), required=False,
        label=u'Категории')

    class Meta:
        model = Promo

    def clean_color(self):
        return self.cleaned_data.get('color', '').lstrip('#')

    def clean(self):
        categories = self.cleaned_data.get('categories')
        value = self.cleaned_data.get('image')
        image = Image.open(value)
        if not categories and image.size[1] != 350:
            raise forms.ValidationError(u'Высота изображения должна быть равна 350 пикселям')

        if categories and image.size[1] != 300:
            raise forms.ValidationError(u'Высота изображения для категории должна быть равна 300 пикселям')

        return self.cleaned_data


class CouponAdminForm(forms.ModelForm):
    products = ProductSelect2MultipleField(label=u'Товары', required=False)
    categories = CategorySelect2MultipleField(label=u'Категории', required=False)

    class Meta:
        model = Coupon

    def clean_code(self):
        return self.cleaned_data.get('code', '').upper().strip()

    def clean_discount_percent(self):
        value = self.cleaned_data.get('discount_percent')
        if 0 >= value >= 100:
            raise forms.ValidationError(u'Процент скидки не может быть больше 100%')

        return value

    def clean(self):
        discount_percent = self.cleaned_data.get('discount_percent')
        discount_amount = self.cleaned_data.get('discount_amount')

        if discount_amount and discount_percent:
            raise forms.ValidationError(u'Нельзя одновременно задавать фиксированную скидку и скидку в процентах')

        if not discount_amount and not discount_percent:
            raise forms.ValidationError(u'Укажите фиксированную скидку или скидку в процентах')

        return self.cleaned_data


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ('code', )

    def __init__(self, net, *args, **kwargs):
        super(CouponForm, self).__init__(*args, **kwargs)
        self.net = net
        self.coupon = None

    def clean_code(self):
        value = self.cleaned_data['code'].upper().strip()

        try:
            self.coupon = Coupon.objects.actual(value)
        except Coupon.DoesNotExist:
            raise forms.ValidationError(u'Извините, этот промо-код недействителен')

        if self.coupon.discount_level and self.coupon.discount_level < self.net:
            raise forms.ValidationError(u'Этот промо-код действителен только при сумме заказа от {} рублей'.format(self.coupon.discount_level))

        return value
