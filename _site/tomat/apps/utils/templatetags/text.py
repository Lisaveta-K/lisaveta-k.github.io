# -*- coding: utf-8 -*-

import re

from django import template
from django.utils.html import mark_safe
from django.conf import settings


register = template.Library()


def quotes(text):
    text = ' %s ' % text.group(0).replace(u'«', '"').replace(u'»', '"').replace(u'„', '"').replace(u'“', '"')

    reg = re.compile(ur'''([\s!\]|#'"\/(;+-])"([^">]*)([^\s"(|])"([^\w])''', re.I | re.S | re.U)

    for i in range(1, 3):
        text = reg.sub(u'\g<1>«\g<2>\g<3>»\g<4>', text)

    while re.findall(ur'«[^»]*«', text):
        text = re.sub(u'«([^»]*)«([^»]*)»', u'«\g<1>„\g<2>“', text, re.S | re.I)

    return text.strip()


@register.filter
def typograph(text):
    text = unicode(text)

    text = re.sub(u'((?s).*)', quotes, text)

    text = re.sub(u'(\d+)\*(\d+)\*(\d+)', u'\g<1>×\g<2>×\g<3>', text, re.S | re.I)
    text = re.sub(u'(\d+)\*(\d+)', u'\g<1>×\g<2>', text, re.S | re.I)

    return text


@register.filter
def integer(value):
    return int(value or 0)


@register.filter
def size(image):
    if not image:
        return ''

    try:
        return mark_safe(u'style="width:%dpx;height:%dpx;"' % (image.width, image.height))
    except (TypeError, IOError):
        if settings.DEBUG:
            return ''
        raise
