# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse

from news.models import News
from products.models import Product


def index(request):
    queryset = News.objects.filter(is_visible=True).order_by('-date_published')
    paginator = Paginator(queryset, 10)

    try:
        objects = paginator.page(request.GET.get('page'))
    except (PageNotAnInteger, EmptyPage):
        objects = paginator.page(1)

    context = {
        'objects': objects,
        'products': Product.objects.for_user(request.user).filter(is_new=True).order_by('?')[:6],
    }

    return render(request, 'news/index.html', context)


def read(request, object_id):
    news = get_object_or_404(News, pk=object_id, is_visible=True)
    latest = News.objects.filter(is_visible=True).exclude(id=news.id).order_by('-date_published')[:10]

    context = {
        'object': news,
        'latest': latest,
    }

    request.breadcrumbs.add(u'Новости', reverse('news.views.index'))

    return render(request, 'news/read.html', context)
