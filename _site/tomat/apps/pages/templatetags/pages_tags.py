# -*- coding: utf-8 -*-

from django import template

from pages.models import Page


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_page(context):
    request = context['request']

    try:
        return Page.objects.get(url=request.path)
    except Page.DoesNotExist:
        pass
