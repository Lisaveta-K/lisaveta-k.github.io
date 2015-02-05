# -*- coding: utf-8 -*-

from django import template

from adverts.models import Promo


register = template.Library()


@register.inclusion_tag('adverts/tags/promo-block.html', takes_context=True)
def promo_block(context, category=None):
    request = context['request']
    objects = Promo.objects.filter(categories=category).order_by('position')
    if request.user.is_authenticated() and request.user.show_wholesale():
        objects = objects.filter(is_wholesale=True)
    else:
        objects = objects.filter(is_retail=True)

    return {
        'category': category,
        'objects': objects,
    }
