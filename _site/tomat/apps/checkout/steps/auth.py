# -*- coding: utf-8 -*-

"""Шаг 1

Авторизация пользователя.

Если пользователь уже авторизирован, переходим к шагу 2
Если пользовать не авторизирован, просим ввести e-mail.

"""

import logging

from satchless.process import InvalidData
from django.contrib.auth import login, authenticate
from django.shortcuts import render

from users.models import User
from checkout.steps.base import Step
from checkout.forms import AuthForm


logger = logging.getLogger(__name__)


class WrongPasswordException(InvalidData):
    pass


class BusyEmailException(InvalidData):
    pass


class AuthStep(Step):
    template = 'checkout/steps/auth.html'

    def __str__(self):
        return 'auth'

    def __init__(self, *args, **kwargs):
        super(AuthStep, self).__init__(*args, **kwargs)

        initial = {}
        if 'email' in self.request.POST:
            initial['email'] = self.request.POST['email']

        self.forms['auth'] = AuthForm(self.request.POST or None, initial=initial)

    def process(self, extra_content=None):
        if self.request.user.is_authenticated():
            return  # Переходим к следующему шагу

        context = extra_content or {}
        context['form'] = self.forms['auth']

        wrong_password = False
        busy_email = False
        try:
            self.validate()
        except InvalidData as e:
            wrong_password = isinstance(e, WrongPasswordException)
            busy_email = isinstance(e, BusyEmailException)
            is_valid = False
        else:
            is_valid = True

        if not is_valid or self.request.method == 'GET':
            context['step'] = self
            context['have_password'] = self.request.POST.get('have_password') == 'yes'
            context['wrong_password'] = wrong_password
            context['busy_email'] = busy_email

            return render(self.request, self.template, context)

        return self.save()

    def validate(self):
        if self.request.user.is_authenticated():
            return

        if not self.forms_are_valid():
            logger.debug('Invalid authentication form')
            raise InvalidData(u'123')

        data = self.forms['auth'].cleaned_data
        email = data['email']
        password = data['password']

        if User.objects.filter(email__iexact=email).exists():
            # Пользователь есть, пробуем авторизировать
            user = authenticate(email=email, password=password)
            if user is not None:
                login(self.request, user)
            elif password:
                logger.debug('Wrong password for email %s' % email)
                raise WrongPasswordException(u'Проверьте правильность пароля')
            else:
                user = User.objects.get(email__iexact=email)
                if not user.has_usable_password():
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(self.request, user)
                else:
                    logger.debug('Email %s is busy' % email)
                    raise BusyEmailException(u'Email уже занят')
        else:
            # Создаем нового пользователя
            user = User(email=email, is_active=True)
            user.set_unusable_password()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            # TODO: ставить флаг, что пользователю надо отправить письмо с паролем
            user.save()

            logger.debug('New user with email %s was created' % email)

            login(self.request, user)

    def save(self):
        """Улыбаемся и машем"""

        pass
