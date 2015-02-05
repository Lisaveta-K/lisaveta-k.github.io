# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from utils.breadcrumbs import Breadcrumbs


class BreadcrumbsMiddleware(object):

    def process_request(self, request):
        request.breadcrumbs = Breadcrumbs()

        if request.path != '/':
            # Сразу добавляем первую хлебную крошку с разделом
            request.breadcrumbs.add(u'Главная', reverse('index'))
