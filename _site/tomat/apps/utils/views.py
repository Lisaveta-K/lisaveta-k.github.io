# -*- coding: utf-8 -*-

from django.http import HttpResponseNotFound
from django.template.loader import render_to_string
from django.template.context import RequestContext

from products.models import Product


def handle404(request, product=None, category=None):
    products = ()
    if product:
        products = list(Product.objects.for_user(request.user).filter(categories=category).exclude(id=product.id) \
                            .only(*Product.LIST_ITEM_REQUIRED_FIELDS).order_by('?')[:8])

    if not products:
        products = Product.objects.for_user(request.user).filter(is_new=True).only(*Product.LIST_ITEM_REQUIRED_FIELDS) \
                       .order_by('?')[:8]

    return HttpResponseNotFound(render_to_string('404.html', {
        'request': request,
        'product': product,
        'products': products,
    }, RequestContext(request)))
