# -*- coding: utf-8 -*-
from bootstrap3_datetime.widgets import DateTimePicker
import datetime

from django import forms
from django.contrib.auth import authenticate
from django.core import validators
from users.heplers import is_friday_after_six_oclock, get_nearest_monday, is_holiday, combine_date_and_time

from users.models import User, Address, Company
from checkout.models import CourierCity


class LoginForm(forms.Form):
    email = forms.EmailField(label=u'E-mail', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label=u'Пароль')

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not email:
            raise forms.ValidationError(u'Введите свой адрес почты')
        if not User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(u'Возможно вы ошиблись в адресе почты?')

        return email

    def clean(self):
        credentials = self.cleaned_data
        if not 'email' in credentials:
            credentials['email'] = ''

        if not authenticate(**credentials):
            raise forms.ValidationError(u'Неправильный email или пароль')

        return credentials


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')


class UserUpdateForm(forms.ModelForm):
    title = forms.CharField(label=u'ФИО', required=True)
    phone = forms.CharField(label=u'Телефон', required=True)

    class Meta:
        model = User
        fields = ('email', 'title', 'phone', 'birthday')


class AddressForm(forms.ModelForm):
    city = forms.CharField(label=u'Город')
    postal_code = forms.CharField(label=u'Индекс')
    street = forms.CharField(label=u'Улица', widget=forms.Textarea(attrs={
        'rows': 2,
    }))
    house = forms.CharField(label=u'Дом')

    class Meta:
        model = Address
        fields = ('city', 'postal_code', 'street', 'house', 'flat', 'email', 'phone', 'receiver_title', 'receiver_phone')


def validate_delivery_datetime(delivery_date, delivery_time=None):
    now = datetime.datetime.now()
    if not delivery_date and delivery_time:
        raise forms.ValidationError(u'Введите дату. Вы ввели только время.')
    delivery_datetime = combine_date_and_time(delivery_date, delivery_time)
    if delivery_datetime:
        if delivery_datetime < now + datetime.timedelta(hours=2):
            raise forms.ValidationError(u'Вы не можете выбрать время доставки раньше, чем через 2 часа от текущего времени')
        if (is_friday_after_six_oclock(now) or is_holiday(now)) and delivery_datetime < get_nearest_monday(now):
            raise forms.ValidationError(u'Вы не можете выбрать дату и время доставки раньше, чем 10:00 ближайшего понедельника')
    return delivery_datetime


class CourierCityAddressForm(AddressForm):
    city = forms.CharField(widget=forms.HiddenInput, required=False)
    courier_city = forms.ModelChoiceField(queryset=CourierCity.objects.all().order_by('id'), label=u'Город',
        help_text=u'Стоимость доставки зависит от выбранного города')
    postal_code = forms.CharField(widget=forms.HiddenInput, required=False)
    delivery_date = forms.DateField(
        label=u'Дата доставки',
        required=False,
        initial=datetime.datetime.today().strftime("%d.%m.%Y"),
        widget=DateTimePicker(options={"format": "DD.MM.YYYY", "pickTime": False}),
    )
    delivery_time = forms.TimeField(
        input_formats=['%H:%M', '%H.%M', '%H-%M', ],
        label=u'Время доставки',
        required=False,
        initial='{}:00'.format((datetime.datetime.now()+datetime.timedelta(hours=3)).time().strftime("%H")),
        widget=DateTimePicker(options={"format": "HH:mm", "pickDate": False, "useMinutes:": False}, icon_attrs={'class': 'glyphicon glyphicon-time'},),
        help_text=u'Доставка осуществляется не ранее, чем через 2 часа после оформления заказа. Если заказ осуществляется с пятницы после 18:00 и до понедельника 09:00, ближайшая доступная доставка не ранее 10:00 понедельника.',
    )

    def clean(self):
        delivery_time = None
        data = self.cleaned_data
        if 'courier_city' in data:
            data['city'] = data['courier_city'].title

        delivery_date = data['delivery_date']
        if 'delivery_time' in data and data['delivery_time']:
            delivery_time = data['delivery_time']
        validate_delivery_datetime(delivery_date, delivery_time)
        data['delivery_time'] = delivery_time
        return data

    class Meta(AddressForm.Meta):
        fields = ('courier_city', 'delivery_date', 'delivery_time', ) + AddressForm.Meta.fields
        exclude = ['postal_code', ]


class DeliveryDateTimeForm(forms.Form):
    delivery_date = forms.DateField(
        label=u'Дата доставки',
        required=False,
        initial=datetime.datetime.today().strftime("%d.%m.%Y"),
        widget=DateTimePicker(options={"format": "DD.MM.YYYY", "pickTime": False}),
    )
    delivery_time = forms.TimeField(
        input_formats=['%H:%M', '%H.%M', '%H-%M', ],
        label=u'Время доставки',
        required=False,
        initial='{}:00'.format((datetime.datetime.now()+datetime.timedelta(hours=3)).time().strftime("%H")),
        widget=DateTimePicker(options={"format": "HH:mm", "pickDate": False, "useMinutes:": False}, icon_attrs={'class': 'glyphicon glyphicon-time'},),
        help_text=u'Доставка осуществляется не ранее, чем через 2 часа после оформления заказа. Если заказ осуществляется с пятницы после 18:00 и до понедельника 09:00, ближайшая доступная доставка не ранее 10:00 понедельника.',
    )

    def clean(self):
        delivery_time = None
        data = self.cleaned_data
        delivery_date = data['delivery_date']
        if 'delivery_time' in data and data['delivery_time']:
            delivery_time = data['delivery_time']
        validate_delivery_datetime(delivery_date, delivery_time)
        data['delivery_time'] = delivery_time
        return data


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'title', 'phone', 'birthday', 'status')


class CompanyForm(forms.ModelForm):
    label = u'Информация о компании'

    phone = forms.CharField(label=u'Телефон', required=True)
    title = forms.CharField(label=u'Название компании', required=True)
    city = forms.CharField(label=u'Город', required=True)
    inn = forms.CharField(label=u'ИНН', required=True, max_length=25)

    class Meta:
        model = Company
        fields = ('director', 'phone', 'title', 'city', 'industry', 'inn', 'ogrn', 'giro',
            'juridical_address', 'post_address',)

    def clean_ogrn(self):
        value = self.cleaned_data.get('ogrn', '').strip()
        if not value:
            return value

        def validate(value, divisor, error_message):
            number = int(value[:-1]) % divisor
            crc = int(value[-1])

            if number > 9:
                last = int(str(number)[-1])
                if last != crc:
                    raise forms.ValidationError(error_message)
                pass  # Валидный код
            elif number == crc:
                pass  # Валидный код
            else:
                raise forms.ValidationError(error_message)

        if len(value) == 13:  # ОГРН
            validate(value, 11, u'Неправильный код ОГРН')
        elif len(value) == 15:  # ОГРНИП
            validate(value, 13, 'Неправильный код ОГРНИП')
        else:
            raise forms.ValidationError(u'Неправильный код ОГРН')

        return value


class RemindForm(forms.Form):
    email = forms.EmailField(label=u'E-mail')

    def clean_email(self):
        value = self.cleaned_data.get('email', '').strip()
        if not User.objects.filter(email=value).exists():
            raise forms.ValidationError(u'Нет пользователя с таким адресом почты')

        return value
