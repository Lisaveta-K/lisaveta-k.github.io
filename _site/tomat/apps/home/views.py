# -*- coding: utf-8 -*-

import logging

from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.core.mail import mail_managers
from annoying.decorators import JsonResponse
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError

from products.models import Category, Product
from news.models import News
from ideas.models import Idea
from shops.models import Delivery
from home.models import Link
from home.forms import FeedbackAnonymousForm, FeedbackForm
from pages.models import Page
from utils.templatetags.text import typograph


logger = logging.getLogger(__name__)


def index(request):
    """Главная страница"""

    products = Product.objects.for_user(request.user).filter(is_new=True).only(*Product.LIST_ITEM_REQUIRED_FIELDS).order_by('?')[:8]
    links = Link.objects.all().order_by('position')

    context = {
        'complementary_categories': Category.objects.filter(is_complementary=True, is_visible=True),
        'new_products': products,
        'ideas': Idea.objects.filter(is_visible=True).order_by('-id')[:4],
        'news': News.objects.filter(is_visible=True).order_by('-date_published')[:2],
        'links': links,
    }

    return render(request, 'home/index.html', context)


def search(request):
    query = request.GET.get('query', '').strip().replace(u'«', '"').replace(u'»', '"')
    try:
        page = int(request.GET.get('page'))
    except (TypeError, ValueError):
        page = 1

    # Делаем редирект, если есть точное совпадение по артикулу
    if query:
        try:
            product = Product.objects.for_user(request.user).filter(sku__iexact=query)[0]
            url = product.get_absolute_url()
            if url:
                return redirect(url)
            else:
                logger.error('Product #%s has no categories' % product.id)
        except IndexError:
            pass

    if page == 1:
        categories = Category.objects.filter(level__in=[0, 2], title__icontains=query, is_visible=True)
    else:
        categories = ()

    products_query = ' & '.join([x.strip() for x in query.split()])
    products_qs = Product.objects.search(products_query, user=request.user)

    paginator = Paginator(products_qs, 20)

    try:
        products = paginator.page(page)
    except EmptyPage:
        products = paginator.page(1)

    news = News.objects.filter(Q(title__icontains=query) | Q(content__icontains=query),
        is_visible=True).order_by('-id')[:3]
    ideas = Idea.objects.filter(Q(title__icontains=query) | Q(content__icontains=query),
        is_visible=True).order_by('-id')[:3]

    context = {
        'query': query,
        'categories': categories,
        'products': products,
        'news': news,
        'ideas': ideas,
        'see_also': Product.objects.for_user(request.user).filter(is_new=True).order_by('?')[:5],
    }

    return render(request, 'home/search.html', context)


def _prepare_obj(instance):
    response = {
        'value': instance.id,
        'title': typograph(instance.title),
        'url': instance.get_absolute_url(),
    }

    photo = instance.get_main_photo()
    if photo:
        try:
            thumb = get_thumbnailer(photo.image).get_thumbnail({
                'size': (60, 60),
                'crop': True,
            })
            response['image'] = thumb.url
        except InvalidImageFormatError:
            pass

    return response


def search_ajax(request):
    query = request.GET.get('query').strip().replace(u'«', '"').replace(u'»', '"')
    if not query:
        return HttpResponseBadRequest()

    try:
        product = Product.objects.for_user(request.user).filter(sku=query)[0]
        return JsonResponse([_prepare_obj(product),])
    except IndexError:
        pass

    products_query = ' & '.join([x.strip() for x in query.split()])
    products_qs = Product.objects.search(products_query, user=request.user)[:5]

    return JsonResponse([_prepare_obj(x) for x in products_qs])


def delivery(request):
    delivery = Delivery.objects.all().order_by('position')
    if request.user.is_authenticated() and request.user.show_wholesale():
        delivery = delivery.filter(is_wholesale=True)
    else:
        delivery = delivery.filter(is_retail=True)

    context = {
        'objects': delivery,
        }

    return render(request, 'home/delivery.html', context)


def wholesale(request):
    page = Page.objects.get(url=request.path)
    children = page.get_children()

    context = {
        'page': page,
        'children': children,
    }

    return render(request, 'home/wholesale.html', context)


def franchisee_credit(request):
    page = Page.objects.get(url=request.path)
    try:
        parent_url = '{0}/'.format(request.path.rsplit('/', 2)[0])
        if parent_url == '/':
            parent_url = request.path
        parent = Page.objects.get(url=parent_url)
    except Page.DoesNotExist:
        children = ()
    else:
        children = list(parent.get_children())
        request.breadcrumbs.add(parent.title, parent.url)

    context = {
        'page': page,
        'children': children,
    }

    return render(request, 'home/franchisee_credit.html', context)

def feedback(request):
    if request.user.is_authenticated():
        form_cls = FeedbackForm
    else:
        form_cls = FeedbackAnonymousForm

    if request.POST:
        form = form_cls(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated():
                instance.user = request.user
            instance.save()

            mail_context = {
                'instance': instance,
            }

            manager_text = render_to_string('home/mail/feedback.txt', mail_context)
            manager_html = render_to_string('home/mail/feedback.html', mail_context)
            mail_managers(u'Новый вопрос на сайте «Томат»', manager_text, html_message=manager_html)

            return HttpResponseRedirect('.?thank=you')

    else:
        form = form_cls()

    context = {
        'form': form,
        'is_sended': 'thank' in request.GET,
    }

    return render(request, 'home/feedback.html', context)
