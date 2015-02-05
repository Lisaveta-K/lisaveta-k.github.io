# -*- coding: utf-8 -*-

from django import template

from products.models import Category


register = template.Library()


@register.inclusion_tag('products/categories/tags/navigation.html')
def navigation(current=None):
    return {
        'categories': Category.objects.filter(level=0, is_visible=True).order_by('position'),
        'current': current,
    }


@register.inclusion_tag('products/categories/tags/list-item.html')
def category_list_item(category):
    return {
        'category': category,
    }


@register.inclusion_tag('products/categories/tags/list-tools.html', takes_context=True)
def category_list_tools(context, page, css_classes='', *args):
    """Пагинатор и сортировка"""

    request = context['request']

    if page.number < 3:
        # Первые 3 страницы
        page_range = page.paginator.page_range[:5]

    elif page.number > page.paginator.num_pages - 3:
        # Последние 3 страницы
        page_range = page.paginator.page_range[-5:]

    else:
        page_range = page.paginator.page_range[page.number - 3:page.number + 2]

    order = request.GET.get('order')
    if not order in ('price', 'title', 'created'):
        order = 'created'

    try:
        price_from = int(request.GET.get('price_from'))
    except (TypeError, ValueError):
        price_from = None

    try:
        price_to = int(request.GET.get('price_to'))
    except (TypeError, ValueError):
        price_to = None

    get_params = {}
    for arg in args:
        value = request.GET.get(arg)
        if value:
            get_params[arg] = value

    return {
        'page': page,
        'page_range': page_range,
        'css_classes': css_classes,
        'showing_all': request.GET.get('show') == 'all',
        'order': order.lstrip('-'),
        'price_from': price_from,
        'price_to': price_to,
        'get_params': get_params,
    }
