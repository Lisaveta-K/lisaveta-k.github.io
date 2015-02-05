# -*- coding: utf-8 -*-

import logging
import datetime
import decimal

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from annoying.decorators import JsonResponse
from django.template import Template, RequestContext
from django.utils.http import is_safe_url

from cart.models import Cart
from cart.forms import CartUpdateForm, CartDeleteForm, ProductSignForm
from checkout.managers import Storage
from adverts.models import Coupon
from adverts.forms import CouponForm
from products.models import Category


logger = logging.getLogger(__name__)


def index(request):
    # TODO: validate coupon

    for item in request.cart:
        if item.product.price_for_user(request.user) is None or not item.product.available_for_user(request.user):
            request.cart.remove(item.product)

    if not len(request.cart):
        return HttpResponseRedirect(reverse('home.views.index'))

    go_back_url = request.GET.get('from', '/')
    if not is_safe_url(go_back_url):
        go_back_url = '/'

    try:
        del request.session[Storage.SESSION_KEY]
    except KeyError:
        pass

    net = request.cart.get_total(request=request).net

    if request.POST:
        coupon_form = CouponForm(net, request.POST)
        if coupon_form.is_valid():
            coupon = coupon_form.coupon
            request.session[Cart.COUPON_KEY] = {
                'id': coupon.id,
                'expires': datetime.datetime.now() + datetime.timedelta(days=1),
            }

            return HttpResponseRedirect('.')
    else:
        coupon_form = CouponForm(net)

    coupon = None
    diff = 0
    is_retail = request.user.is_anonymous() or not request.user.show_wholesale()
    if is_retail and Cart.COUPON_KEY in request.session:
        data = request.session[Cart.COUPON_KEY]
        try:
            coupon = Coupon.objects.get(id=data['id'])
            if data['expires'] < datetime.datetime.now():
                raise Coupon.DoesNotExist()
        except Coupon.DoesNotExist:
            del request.session[Cart.COUPON_KEY]

    if is_retail and coupon:
        matches = []
        products_ids = list(coupon.products.all().values_list('id', flat=True))
        categories_ids = list(coupon.categories.all().values_list('id', flat=True))

        for item in request.cart:
            if products_ids or categories_ids:
                if item.product.id in products_ids:
                    matches.append(item)
                    continue

                for category_id in item.product.categories.all().values_list('id', flat=True):
                    if category_id in categories_ids:
                        matches.append(item)
                        continue
            else:  # поля категории и товары не заполнены - делаем скидку на всё
                matches.append(item)

        matches = list(set(matches))

        # Сумма стоимости всех товаров
        amount = sum([x.product.price_for_user(request.user) * x.quantity for x in matches])
        if coupon.discount_percent:
            diff = decimal.Decimal((float(amount) / 100.0) * coupon.discount_percent)
        else:
            diff = coupon.discount_amount
        net = round(net - diff, 2)

    context = {
        'cart': request.cart,
        'total': net,
        'go_back_url': go_back_url,
        'coupon_form': coupon_form,
        'coupon': coupon,
        'diff': round(diff, 2),
        'complementary_categories': Category.objects.filter(is_complementary=True, is_visible=True),
    }

    return render(request, 'cart/index.html', context)


@require_POST
def update(request):
    """Добавление нового товара в корзину

    Если товар уже есть в корзине, изменяется количество единиц в нем

    Параметры::
        id: идентификатор товара `products.models.Product`
        quantity: количество единиц
    """

    form = CartUpdateForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    product = form.cleaned_data['product']
    quantity = form.cleaned_data['quantity']
    replace = form.cleaned_data['replace']
    # TODO: sanitize redirect URI
    redirect_url = request.POST.get('next')

    if not product.available_for_user(request.user):
        return HttpResponseBadRequest()

    # Временная заглушка
    if product.price_for_user(request.user) is not None:
        request.cart.add(product, quantity, replace=replace)
    else:
        logger.error('Got an empty price product #%d from page %s' % (product.id, request.META.get('HTTP_REFERER')))

    source = request.POST.get('source', '').strip()

    coupon = None
    diff = 0
    net = request.cart.get_total(request=request).net
    if Cart.COUPON_KEY in request.session:
        data = request.session[Cart.COUPON_KEY]
        try:
            coupon = Coupon.objects.get(id=data['id'])
            if data['expires'] < datetime.datetime.now():
                raise Coupon.DoesNotExist()
        except Coupon.DoesNotExist:
            del request.session[Cart.COUPON_KEY]

    if coupon:
        matches = []
        products_ids = list(coupon.products.all().values_list('id', flat=True))
        categories_ids = list(coupon.categories.all().values_list('id', flat=True))

        for item in request.cart:
            if item.product.id in products_ids:
                matches.append(item)
                continue

            for category_id in item.product.categories.all().values_list('id', flat=True):
                if category_id in categories_ids:
                    matches.append(item)
                    continue

        matches = list(set(matches))

        # Сумма стоимости всех товаров
        amount = sum([x.product.price_for_user(request.user) * x.quantity for x in matches])
        if coupon.discount_percent:
            diff = decimal.Decimal((float(amount) / 100.0) * coupon.discount_percent)
        else:
            diff = coupon.discount_amount
        net = round(net - diff, 2)

    if request.is_ajax():
        if source == 'cart':
            # Обновляем данные корзины
            return JsonResponse({
                'item_total': (u'%.2f' % request.cart.price(product, request=request)).replace('.', ','),
                'net': (u'%.2f' % net).replace('.', ','),
                'coupon': (u'%.2f' % float(diff)).replace('.', ','),
            })

        elif source == 'form-small':
            return render(request, 'cart/update_ajax_small.html', {
                'in_cart': request.cart.quantity(product),
            })

        return render(request, 'cart/update_ajax.html', {
            'from_url': redirect_url,
            'quantity': request.cart.quantity(product),
            'product': product,
        })

    return HttpResponseRedirect(redirect_url)


@require_POST
def delete(request):
    """Удаление товара из корзины

    Параметры::
        id: идентификатор товара `products.models.Product`
        quantity: количество единиц

    Если не указан параметр `quantity`, удаляются все товары
    """

    form = CartDeleteForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    product = form.cleaned_data['product']
    # TODO: sanitize redirect URI
    redirect_url = request.POST.get('next')

    request.cart.add(product, 0, replace=True)  # removing it

    if request.is_ajax():
        return JsonResponse({})

    return HttpResponseRedirect(redirect_url)


@require_POST
def clear(request):
    try:
        del request.session[Cart.SESSION_KEY]
    except KeyError:
        pass

    if request.is_ajax():
        return JsonResponse({})

    # TODO: sanitize URL
    redirect_url = request.POST.get('from', '/')

    return HttpResponseRedirect(redirect_url)

_reload_template = Template(u'''{% load cart_tags %}{% cart_widget %}''')


def reload(request):
    context = RequestContext(request)

    return HttpResponse(_reload_template.render(context))


def status(request):
    net = request.cart.get_total(request=request).net

    coupon = None
    diff = 0
    net = request.cart.get_total(request=request).net
    if Cart.COUPON_KEY in request.session:
        data = request.session[Cart.COUPON_KEY]
        try:
            coupon = Coupon.objects.get(id=data['id'])
            if data['expires'] < datetime.datetime.now():
                raise Coupon.DoesNotExist()
        except Coupon.DoesNotExist:
            del request.session[Cart.COUPON_KEY]

    if coupon:
        matches = []
        products_ids = list(coupon.products.all().values_list('id', flat=True))
        categories_ids = list(coupon.categories.all().values_list('id', flat=True))

        for item in request.cart:
            if item.product.id in products_ids:
                matches.append(item)
                continue

            for category_id in item.product.categories.all().values_list('id', flat=True):
                if category_id in categories_ids:
                    matches.append(item)
                    continue

        matches = list(set(matches))

        # Сумма стоимости всех товаров
        amount = sum([x.product.price_for_user(request.user) * x.quantity for x in matches])
        if coupon.discount_percent:
            diff = decimal.Decimal((float(amount) / 100.0) * coupon.discount_percent)
        else:
            diff = coupon.discount_amount
        net = round(net - diff, 2)

    return JsonResponse({
        'net': (u'%.2f' % net).replace('.', ','),
        'coupon': (u'%.2f' % float(diff)).replace('.', ','),
    })


@require_POST
def sign(request):
    form = ProductSignForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest()

    product = form.cleaned_data['product']

    for item in request.cart:
        if item.product == product:
            if item.data is None:
                item.data = {}
            item.data['sign'] = form.cleaned_data['text']
            request.cart.modified = True
            break

    return JsonResponse({})
