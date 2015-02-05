# -*- coding: utf-8 -*-

import json

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from shops.models import Shop, City


def index(request):
    """Список городов с магазинами"""

    context = {
        'cities': City.objects.all().order_by('id'),
    }

    return render(request, 'shops/index.html', context)


def read(request, city_slug):
    """Просмотр списка магазинов в одном городе"""

    city = get_object_or_404(City, slug=city_slug)
    shops = list(city.shops.all().order_by('position'))
    points = {}
    for shop in shops:
        if shop.point:
            points[shop.id] = shop.point.coords

    context = {
        'city': city,
        'shops': list(shops),
        'points': json.dumps(points),
    }

    request.breadcrumbs.add(u'Наши магазины', reverse('shops.views.index'))

    return render(request, 'shops/read.html', context)
