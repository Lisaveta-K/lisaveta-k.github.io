# -*- coding: utf-8 -*-

import logging
import requests
import hashlib

from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.conf import settings

from robokassa.models import SuccessNotification
from robokassa.forms import ResultURLForm, SuccessRedirectForm, FailRedirectForm
from robokassa.signals import fail_page_visited
from checkout.helpers import send_order_mails
from checkout.managers import Checkout, Storage
from checkout.models import Order


logger = logging.getLogger(__name__)


@csrf_exempt
def step(request, step):
    if not request.cart:
        return redirect('cart.index')

    checkout = Checkout(request)
    if not step:
        return redirect(checkout.get_next_step())
    try:
        step = checkout[step]
    except KeyError:
        raise Http404()

    response = step.process()

    return response or redirect(checkout.get_next_step())


@csrf_exempt
def receive_result(request):
    """ обработчик для ResultURL. """

    form = ResultURLForm(request.POST)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        # сохраняем данные об успешном уведомлении в базе, чтобы
        # можно было выполнить дополнительную проверку на странице успешного
        # заказа
        notification = SuccessNotification.objects.create(InvId=id, OutSum=sum)

        order = Order.objects.get(id=id)
        order.status = Order.STATUS_PAYED
        order.net = float(sum)
        logger.info('Order #%d had payed. Sum: %s' % (order.id, order.net))
        if not order.is_emails_sended:
            send_order_mails(order, order.user)
            order.is_emails_sended = True
        order.save()

        return HttpResponse('OK%s' % id)

    return HttpResponse('error: bad signature')


@csrf_exempt
def success(request):
    """ обработчик для SuccessURL """

    form = SuccessRedirectForm(request.POST or request.GET)
    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        url = reverse('checkout.step', args=('receipt', ))
        return HttpResponseRedirect('%s?order=%s' % (url, id))

    return render(request, 'robokassa/error.html', {'form': form})


@csrf_exempt
def fail(request):
    """ обработчик для FailURL """

    form = FailRedirectForm(request.POST or request.GET)

    try:
        del request.session[Storage.SESSION_KEY]
    except KeyError:
        pass

    if form.is_valid():
        id, sum = form.cleaned_data['InvId'], form.cleaned_data['OutSum']

        fail_page_visited.send(sender=form, InvId=id, OutSum=sum, extra=form.extra_params())

        context = {'InvId': id, 'OutSum': sum, 'form': form}
        context.update(form.extra_params())

        return render(request, 'robokassa/fail.html', context)

    return render(request, 'robokassa/error.html', {'form': form})


@csrf_exempt
def rk_test_start(request):
    sum = request.GET['OutSum']
    order_id = request.GET['InvId']

    if request.POST:
        signature = hashlib.md5( ':'.join([sum, order_id, settings.ROBOKASSA_PASSWORD2]) ).hexdigest().upper()
        url = 'http://tomat.local%s' % reverse('robokassa_result')
        response = requests.post(url, data={
            'OutSum': sum,
            'InvId': order_id,
            'SignatureValue': signature,
            'Culture': 'ru',
        })
        assert response.content == 'OK%s' % order_id

        url = '%s?OutSum=%s&InvId=%s&Culture=ru&SignatureValue=%s' % (
            reverse('robokassa_success'),
            sum,
            order_id,
            signature,
        )
        return HttpResponseRedirect(url)

    context = {
        'sum': sum,
        'order_id': order_id,
    }

    return render(request, 'robokassa/test-start.html', context)
