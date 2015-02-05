# -*- coding: utf-8 -*-

from django import template

from cart.models import Cart
from cart.forms import CartUpdateForm, ProductSignForm


register = template.Library()


@register.inclusion_tag('cart/tags/form.html', takes_context=True)
def cart_form(context, product):
    request = context['request']

    form = CartUpdateForm(initial={
        'product': product.id,
    })

    return {
        'product': product,
        'request': request,
        'form': form,
        'quantity': request.cart.quantity(product),
    }


@register.inclusion_tag('cart/tags/widget.html', takes_context=True)
def cart_widget(context):
    request = context['request']

    if len(request.cart):
        total = request.cart.get_total(request=request).net
    else:
        total = None

    from_url = request.GET.get('from', request.path)

    return {
        'from_url': from_url,
        'cart': request.session[Cart.SESSION_KEY],
        'total': total,
    }


@register.inclusion_tag('cart/tags/form_small.html', takes_context=True)
def cart_form_small(context, product):
    request = context['request']

    from_url = request.GET.get('from', request.path)

    form = CartUpdateForm(initial={
        'product': product.id,
    })

    return {
        'request': request,
        'form': form,
        'in_cart': request.cart.quantity(product),
        'from_url': from_url,
    }


@register.simple_tag(takes_context=True)
def get_item_price(context, item):
    request = context['request']

    return ('%10.2f' % item.get_total(request=request).net).replace('.', ',')

@register.simple_tag(takes_context=True)
def get_product_price(context, product):
    request = context['request']

    return ('%10.2f' % product.price_for_user(request.user)).replace('.', ',')


@register.inclusion_tag('cart/tags/form_sign.html')
def sign_form(product):
    initial = {
        'product': product.product,
    }
    have_text = False
    if product.data:
        initial['text'] = product.data.get('sign')
        have_text = True
    form = ProductSignForm(initial=initial)

    return {
        'form': form,
        'have_text': have_text,
    }
