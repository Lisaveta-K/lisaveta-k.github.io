# -*- coding: utf-8 -*-
from captcha.fields import CaptchaField

from django import forms

from home.models import Feedback


class FeedbackAnonymousForm(forms.ModelForm):
    title = forms.CharField(label=u'Ваше имя', required=True)
    captcha = CaptchaField(label=u'Введите символы')

    class Meta:
        model = Feedback
        fields = ('title', 'email', 'content')


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ('content', )
