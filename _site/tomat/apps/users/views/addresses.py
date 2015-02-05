# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from users.models import Address, User
from users.forms import AddressForm


def index(request):
    """Список всех адресов доставки пользователя"""

    addresses = Address.objects.filter(user=request.user, is_deleted=False)

    context = {
        'addresses': addresses,
    }

    return render(request, 'users/addresses/index.html', context)


def create(request):
    """Добавление нового адреса доставки"""

    initial = {
        'email': request.user.email,
    }
    # TODO: Возможно, заполнять только для розничных покупателей?
    if request.user.title:
        initial['receiver_title'] = request.user.title
    if request.user.phone:
        initial['phone'] = request.user.phone

    if request.POST:
        form = AddressForm(request.POST, initial=initial)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            return HttpResponseRedirect(reverse('users.address.index'))

    else:
        form = AddressForm(initial=initial)

    context = {
        'form': form,
    }

    return render(request, 'users/addresses/create.html', context)


def update(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.POST:
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            return HttpResponseRedirect(reverse('users.address.index'))

    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
    }

    return render(request, 'users/addresses/update.html', context)


@login_required
@require_POST
def delete(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.is_deleted = True
    address.save()

    return HttpResponseRedirect(reverse('users.address.index'))
