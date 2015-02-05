# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login as user_login, logout as user_logout, authenticate
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from users.models import User
from users.forms import RegisterForm, LoginForm, RemindForm, CompanyForm
from products.models import Product


def login(request):
    """Авторизация пользователей"""

    if request.user.is_authenticated():
        return redirect('/')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            user_login(request, user)

            # TODO: вынести в `cart.helpers`
            for item in request.cart:
                if item.product.price_for_user(user) is None or not item.product.available_for_user(user):
                    request.cart.remove(item.product)

            redirect_url = request.GET.get('next', '/')

            return redirect(redirect_url)


    else:
        form = LoginForm()

    context = {
        'form': form,
    }

    return render(request, 'users/auth/login.html', context)


def logout(request):
    user_logout(request)

    redirect_url = request.GET.get('next', '/')

    return redirect(redirect_url)


def register(request):
    """Регистрация нового пользователя"""

    if request.POST:
        if request.POST.get('type') == 'wholesale':
            return redirect(reverse('users.auth.register.wholesale'))

        form = RegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(form.cleaned_data['password'])
            instance.save()
            instance = authenticate(email=instance.email, password=form.cleaned_data['password'])
            user_login(request, instance)

            return redirect(reverse('users.auth.register.completed'))

    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, 'users/auth/register.html', context)


def register_wholesale(request):
    """Регистрация оптового покупателя"""

    if request.POST:
        form = RegisterForm(request.POST)
        company_form = CompanyForm(request.POST)

        if form.is_valid() and company_form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(form.cleaned_data['password'])
            instance.status = User.STATUS_WHOLESALE
            instance.save()

            instance = authenticate(email=instance.email, password=form.cleaned_data['password'])
            user_login(request, instance)

            company = company_form.save(commit=False)
            company.user = request.user
            company.save()

            return redirect(reverse('users.auth.register.completed'))

    else:
        form = RegisterForm()
        company_form = CompanyForm()

    context = {
        'form': form,
        'company_form': company_form,
    }

    return render(request, 'users/auth/register_wholesale.html', context)


def registration_completed(request):
    products = Product.objects.for_user(request.user).filter(is_new=True).only(*Product.LIST_ITEM_REQUIRED_FIELDS).order_by('?')[:8]

    context = {
        'products': products,
    }

    return render(request, 'users/auth/register_completed.html', context)


def remind(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    is_sended = 'check-your-email' in request.GET

    if request.POST:
        form = RemindForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data['email'])
            password = get_random_string(5, 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789').upper()
            user.set_password(password)
            user.save()

            context = {
                'user': user,
                'password': password,
            }

            user_text = render_to_string('users/mail/remind.txt', context)
            user_html = render_to_string('users/mail/remind.html', context)
            message = EmailMultiAlternatives(u'Новый пароль для интернет-магазина «Томат»', user_text,
                settings.EMAIL_FROM, [user.email, ])
            message.attach_alternative(user_html, 'text/html')
            message.send()

            return HttpResponseRedirect('.?check-your-email')

    else:
        form = RemindForm()

    context = {
        'is_sended': is_sended,
        'form': form,
    }

    return render(request, 'users/auth/remind.html', context)
