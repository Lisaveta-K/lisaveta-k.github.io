# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse

from users.models import User


register = template.Library()


@register.inclusion_tag('products/products/tags/list-item.html', takes_context=True)
def product_list_item(context, product, parent_category=None, category=None):
    """Рендерим блок отдельного товара в списке товаров"""

    request = context['request']

    if parent_category and category:
        url = reverse('products.views.products.read', args=(parent_category.slug, category.slug, product.id, product.slug))
    else:
        url = product.get_absolute_url()

    try:
        photo = product.photos.all().order_by('-is_main')[0]
    except IndexError:
        photo = None

    return {
        'request': context['request'],
        'product': product,
        'photo': photo,
        'url': url,
        'have_discount': product.has_discount(request.user),
    }


@register.inclusion_tag('products/products/tags/price.html', takes_context=True)
def product_price(context, product):
    request = context['request']

    price, discount = None, None
    if request.user.is_anonymous() or request.user.status in (User.STATUS_CUSTOMER, User.STATUS_ADMIN):
        price = int(product.price or 0)
        discount = int(product.discount or 0)
    else:
        if request.user.is_wholesale:
            price = product.wholesale_price
            discount = product.wholesale_discount
        else:
            price = product.franchisee_price
            discount = product.franchisee_discount

    return {
        'price': price,
        'discount': discount,
    }


_all_amount = u'''<div class="per-pack-amount" title="Количество в упаковке / количество в коробке">%s/%s</div>'''
_pack_amount = u'''<div class="per-pack-amount" title="Количество в упаковке">%s</div>'''

@register.simple_tag(takes_context=True)
def product_pack_amount(context, product):
    request = context['request']

    if request.user.is_anonymous() or not request.user.show_wholesale():
        return ''

    if product.pack_amount and product.box_amount:
        return _all_amount % (product.pack_amount, product.box_amount)

    return _pack_amount % product.pack_amount
