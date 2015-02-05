# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from pages.models import Page


def read(request, url):
    page = get_object_or_404(Page, url=url)
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

    return render(request, 'pages/read.html' if not children else 'pages/read_lc.html', context)
