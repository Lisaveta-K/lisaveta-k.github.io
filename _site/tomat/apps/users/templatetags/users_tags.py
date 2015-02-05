# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse_lazy, reverse


register = template.Library()


NAVIGATION_URLS = (
    (reverse_lazy('users.user.update'), u'Моя информация'),
    (reverse_lazy('users.orders.index'), u'Мои заказы'),
    (reverse_lazy('users.address.index'), u'Адреса доставки'),
)

@register.inclusion_tag('users/tags/navigation.html', takes_context=True)
def user_navigation(context):
    request = context['request']

    urls = []
    for url, title in NAVIGATION_URLS:
        urls.append([None if request.path == str(url) else url, title])

    if request.user.show_wholesale():
        url = reverse('users.company.update')
        urls.append((None if request.path == url else url, u'Моя компания'))

    return {
        'urls': urls,
    }
