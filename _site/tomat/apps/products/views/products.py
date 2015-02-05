# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponsePermanentRedirect, Http404

from products.models import Category, Product
from shops.models import Delivery
from utils.views import handle404


def read(request, parent_slug, slug, product_id):
    """Просмотр информации о товаре"""

    category_parent = get_object_or_404(Category, slug=parent_slug)
    try:
        category = Category.objects.get(slug=slug, parent__in=category_parent.children.all(), is_visible=True)
    except Category.DoesNotExist:
        category = Category.objects.get(slug=slug, parent=category_parent, is_visible=True)
    product = get_object_or_404(Product, categories=category, id=product_id)
    # , is_visible=True, quantity__gt=0
    if not product.is_visible or product.quantity <= 0:
        return handle404(request, product, category)

    if request.user.is_anonymous():
        if not product.is_retail:
            raise Http404()
    else:
        if request.user.show_wholesale() and not product.is_wholesale:
            raise Http404()
        elif not request.user.show_wholesale() and not product.is_retail:
            raise Http404()

    similar = Product.objects.for_user(request.user).filter(categories=category).exclude(id=product.id).order_by('?')
    if request.user.is_authenticated() and request.user.show_wholesale():
        similar = similar[:10]
    else:
        similar = similar[:6]

    delivery = Delivery.objects.all().order_by('position')
    if request.user.is_authenticated() and request.user.show_wholesale():
        delivery = delivery.filter(is_wholesale=True)
    else:
        delivery = delivery.filter(is_retail=True)

    price = int(product.price or 0)
    discount = int(product.discount or 0)
    if request.user.is_authenticated():
        if request.user.is_wholesale:
            price = product.wholesale_price
            discount = product.wholesale_discount
        elif request.user.is_franchisee:
            price = product.franchisee_price
            discount = product.franchisee_discount

    # Сопутствующие категории, только для розницы
    if request.user.is_anonymous() or (request.user.is_authenticated() and not request.user.show_wholesale()):
        complementary_categories = Category.objects.filter(is_complementary=True, is_visible=True)
    else:
        complementary_categories = ()

    context = {
        'category': category,
        'category_parent': category_parent,
        'product': product,
        'photos': list(product.photos.all().order_by('-is_main')),
        'similar': similar,
        'complementary_categories': complementary_categories,
        'delivery': delivery,
        'price': price,
        'discount': discount,
    }

    request.breadcrumbs.add(category_parent.title, category_parent.get_absolute_url())
    request.breadcrumbs.add(category.title, category.get_absolute_url())

    return render(request, 'products/products/read.html', context)


def legacy_redirect(request, product_id):
    """Переадресация продуктов со старых ссылок"""

    product = get_object_or_404(Product, id=product_id)
    url = product.get_absolute_url()
    if url is None:
        raise Http404()

    return HttpResponsePermanentRedirect(url)


def fast_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    price = int(product.price or 0)
    discount = int(product.discount or 0)
    if request.user.is_authenticated():
        if request.user.is_wholesale:
            price = product.wholesale_price
            discount = product.wholesale_discount
        elif request.user.is_franchisee:
            price = product.franchisee_price
            discount = product.franchisee_discount

    context = {
        'product': product,
        'user': request.user,
        'price': price,
        'discount': discount,
    }

    return render(request, 'products/products/fast_view.html', context)
