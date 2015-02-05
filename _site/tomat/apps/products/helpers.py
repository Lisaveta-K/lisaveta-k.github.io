# -*- coding: utf-8 -*-

import math
try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    from xml.etree import ElementTree

from django.db.models import Min, Max


def prices_filter(queryset, current_min=None, current_max=None):

    min_price = queryset.aggregate(Min('price'))['price__min']
    max_price = queryset.aggregate(Max('price'))['price__max']
    if not min_price or not max_price:
        return ()


    step_price = 500
    steps_amount = math.ceil((max_price - min_price) / step_price)
    if steps_amount > 5:
        step_price = 1000
        steps_amount = math.ceil((max_price - min_price) / step_price)

    if steps_amount > 10:
        step_price = 5000
        steps_amount = math.ceil((max_price - min_price) / step_price)

    steps = []

    step_idx = 0
    while step_idx < steps_amount:
        step_min = step_idx * step_price
        step_max = step_min + step_price
        products_cnt = None
        while products_cnt is None:
            if step_idx == 0:
                products_cnt = queryset.filter(price__lte=step_max).count()
            elif step_idx == steps_amount - 1:
                products_cnt = queryset.filter(price__gte=step_min).count()
            else:
                products_cnt = queryset.filter(price__range=(step_min, step_max)).count()

            if products_cnt == 0:
                step_max += step_price
                steps_amount -= 1
                products_cnt = None
                continue
            else:
                break

        if step_idx == 0:
            step_min = None
        elif step_idx == steps_amount - 1:
            step_max = None

        is_current = current_min == step_min and current_max == step_max
        steps.append([step_min, step_max, products_cnt, is_current])

        step_idx += 1

    if len(steps) == 1:
        return ()

    return steps


def parse_1c(content):
    root = ElementTree.fromstring(content)
    for item in root.iter('Item'):
        code = item.find('Code').text
        price = float(item.find('Price').text)
        quantity = int(float(item.find('Ost').text))
        if quantity < 0:
            quantity = 0

        yield code, price, quantity
