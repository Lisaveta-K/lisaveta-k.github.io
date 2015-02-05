# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from users.forms import UserUpdateForm
from users.models import Address
from checkout.models import Order, OrderItem


@login_required
def update(request):
    if request.POST:
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('.')

    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
        'have_addresses': Address.objects.filter(user=request.user, is_deleted=False).exists(),
    }

    return render(request, 'users/user/update.html', context)
