# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from products.models import Category, Product
from products.helpers import prices_filter
from users.models import User


ORDER_MAPPING = {
    User.STATUS_ADMIN: 'price',
    User.STATUS_CUSTOMER: 'price',
    User.STATUS_WHOLESALE: 'wholesale_price',
    User.STATUS_FRANCHISEE: 'franchisee_price',
}


def parent(request, slug):
    """Просмотр родительской категории и списка под-категорий"""

    category = get_object_or_404(Category, slug=slug, parent__isnull=True, is_visible=True)
    children = list(Category.objects.filter(parent__in=category.children.filter(is_visible=True), is_visible=True).prefetch_related('parent'))
    standalone = list(Category.objects.filter(parent=category, is_standalone=True, is_visible=True))
    for item in standalone:
        item.parent = category
    children += standalone

    children = sorted(children, key=lambda x: x.parent_id)

    objects = ()
    show = 'show' in request.GET
    if show:
        order = request.GET.get('order')
        if not order in ('price', 'title', 'created'):
            order = 'created'
        if order == 'created':
            order = '-created'

        try:
            price_from = int(request.GET.get('price_from'))
        except (TypeError, ValueError):
            price_from = None

        try:
            price_to = int(request.GET.get('price_to'))
        except (TypeError, ValueError):
            price_to = None

        if order == 'price':
            if request.user.is_anonymous():
                order_field = ORDER_MAPPING[User.STATUS_CUSTOMER]
            else:
                order_field = ORDER_MAPPING[request.user.status]
        else:
            order_field = order

        queryset = Product.objects.for_user(request.user).filter(categories__in=children)

        kwargs = {}
        if price_from:
            kwargs['price__gte'] = price_from
        if price_to:
            kwargs['price__lte'] = price_to

        queryset = queryset.filter(**kwargs).order_by(order_field).only(*Product.LIST_ITEM_REQUIRED_FIELDS).distinct()

        try:
            page = int(request.GET.get('page'))
        except (TypeError, ValueError):
            page = 1

        paginator = Paginator(queryset, 20)

        try:
            objects = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            objects = paginator.page(1)

    context = {
        'category': category,
        'children': children,
        'objects': objects,
    }

    return render(request, 'products/categories/parent.html', context)


def read(request, parent_slug, slug):
    """Просмотр списка товаров отдельной категории"""

    parent = get_object_or_404(Category, slug=parent_slug, parent__isnull=True)
    parents_ids = list(parent.direct_children().values_list('id', flat=True))

    try:
        # Категория третьего уровня
        category = Category.objects.get(slug=slug, parent__in=parents_ids, is_visible=True)
        other_categories = Category.objects.filter(parent__in=parents_ids, is_visible=True).exclude(id=category.id)
    except Category.DoesNotExist:
        # Категория второго уровня
        category = get_object_or_404(Category, slug=slug, parent=parent, is_visible=True)

        other_categories = Category.objects.filter(parent=parent, is_visible=True, is_standalone=True).exclude(id=category.id)
        if not other_categories.exists():
            other_categories = Category.objects.filter(parent__in=parents_ids, is_visible=True).exclude(id=category.id)

    if category.is_complementary and not category.is_standalone and not category.products.exists():
        request.breadcrumbs.add(parent.title, parent.get_absolute_url())

        context = {
            'category': category,
            'children': category.direct_children(),
        }
        return render(request, 'products/categories/parent.html', context)

    other_categories = other_categories.order_by('?')[:5]

    show_all = request.GET.get('show') == 'all'

    order = request.GET.get('order')
    if not order in ('price', 'title', 'created'):
        order = 'created'
    if order == 'created':
        order = '-created'

    try:
        price_from = int(request.GET.get('price_from'))
    except (TypeError, ValueError):
        price_from = None

    try:
        price_to = int(request.GET.get('price_to'))
    except (TypeError, ValueError):
        price_to = None

    if order == 'price':
        if request.user.is_anonymous():
            order_field = ORDER_MAPPING[User.STATUS_CUSTOMER]
        else:
            order_field = ORDER_MAPPING[request.user.status]
    else:
        order_field = order

    queryset = Product.objects.for_user(request.user).filter(categories=category)

    kwargs = {}
    if price_from:
        kwargs['price__gte'] = price_from
    if price_to:
        kwargs['price__lte'] = price_to

    products = queryset.filter(**kwargs).order_by(order_field).only(*Product.LIST_ITEM_REQUIRED_FIELDS)

    if show_all:
        products_cnt = products.count()
        paginator = Paginator(products, products_cnt)
    else:
        paginator = Paginator(products, 20)

    try:
        page = int(request.GET.get('page'))
    except (TypeError, ValueError):
        page = 1
    try:

        objects = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        objects = paginator.page(1)

    context = {
        'category_parent': parent,
        'category': category,
        'objects': objects,
        'other_categories': other_categories,
        'prices': list(prices_filter(queryset, price_from, price_to)),
        # GET params
        'order': order.lstrip('-'),
        'price_from': price_from,
        'price_to': price_to,
        'show_all': show_all,
        'page': page,
    }

    request.breadcrumbs.add(parent.title, parent.get_absolute_url())

    return render(request, 'products/categories/read.html', context)


def new(request):
    """Список новых товаров вперемешку"""

    show_all = request.GET.get('show') == 'all'

    order = request.GET.get('order')
    if not order in ('price', 'title', 'created'):
        order = 'created'
    if order == 'created':
        order = '-created'

    try:
        price_from = int(request.GET.get('price_from'))
    except (TypeError, ValueError):
        price_from = None

    try:
        price_to = int(request.GET.get('price_to'))
    except (TypeError, ValueError):
        price_to = None

    if order == 'price':
        if request.user.is_anonymous():
            order_field = ORDER_MAPPING[User.STATUS_CUSTOMER]
        else:
            order_field = ORDER_MAPPING[request.user.status]
    else:
        order_field = order

    queryset = Product.objects.for_user(request.user).filter(is_new=True)

    kwargs = {}
    if price_from:
        kwargs['price__gte'] = price_from
    if price_to:
        kwargs['price__lte'] = price_to

    products = queryset.filter(**kwargs).order_by(order_field).only(*Product.LIST_ITEM_REQUIRED_FIELDS)

    if show_all:
        products_cnt = products.count()
        paginator = Paginator(products, products_cnt)
    else:
        paginator = Paginator(products, 20)

    try:
        page = int(request.GET.get('page'))
    except (TypeError, ValueError):
        page = 1
    try:

        objects = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        objects = paginator.page(1)

    context = {
        'category_parent': parent,
        'objects': objects,
        'prices': list(prices_filter(queryset, price_from, price_to)),
        # GET params
        'order': order.lstrip('-'),
        'price_from': price_from,
        'price_to': price_to,
        'show_all': show_all,
        'page': page,
    }

    return render(request, 'products/categories/new.html', context)