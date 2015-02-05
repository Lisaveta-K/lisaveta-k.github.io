# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.core.paginator import PageNotAnInteger, InvalidPage, Paginator
from django.core.urlresolvers import reverse

from ideas.models import Idea, Category
from products.models import Product


def index(request):
    queryset = Idea.objects.filter(is_visible=True).order_by('-id')

    paginator = Paginator(queryset, 6)

    try:
        objects = paginator.page(request.GET.get('page'))
    except (InvalidPage, PageNotAnInteger):
        objects = paginator.page(1)

    context = {
        'categories': Category.objects.all().order_by('id'),
        'objects': objects,
    }

    return render(request, 'ideas/index.html', context)


def category(request, category_slug):
    """Список идей подарков определенной категории"""

    category = get_object_or_404(Category, slug=category_slug)
    queryset = Idea.objects.filter(category=category, is_visible=True).order_by('-id')

    paginator = Paginator(queryset, 6)

    try:
        objects = paginator.page(request.GET.get('page'))
    except (InvalidPage, PageNotAnInteger):
        objects = paginator.page(1)

    context = {
        'categories': Category.objects.all().order_by('id'),
        'objects': objects,
    }

    request.breadcrumbs.add(u'Идеи подарков', reverse('ideas.views.index'))

    return render(request, 'ideas/index.html', context)


def read(request, category_slug, idea_id):
    category = get_object_or_404(Category, slug=category_slug)
    idea = get_object_or_404(Idea, pk=idea_id, is_visible=True, category=category)
    idea.category = category

    products = Product.objects.for_user(request.user).filter(ideas=idea)

    context = {
        'object': idea,
        'products': products,
    }

    request.breadcrumbs.add(u'Идеи подарков', reverse('ideas.views.index'))
    request.breadcrumbs.add(category.title, category.get_absolute_url())

    return render(request, 'ideas/read.html', context)
