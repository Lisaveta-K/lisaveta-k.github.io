# -*- coding: utf-8 -*-

from django import template

from shops.models import City


register = template.Library()


@register.assignment_tag
def get_cities():
    return City.objects.all().order_by('id')
