# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from checkout.models import Order, OrderItem


@login_required
def index(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')

    context = {
        'orders': orders,
    }

    return render(request, 'users/orders/index.html', context)


@login_required
def read(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = OrderItem.objects.filter(order=order).select_related('product')

    context = {
        'order': order,
        'items': items,
    }

    request.breadcrumbs.add(u'Мои заказы', reverse('users.orders.index'))

    return render(request, 'users/orders/read.html', context)
