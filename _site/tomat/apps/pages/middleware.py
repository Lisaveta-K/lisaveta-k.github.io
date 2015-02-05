# -*- coding: utf-8 -*-

from django.http import Http404
from django.conf import settings

from pages.views import read


class PageFallbackMiddleware(object):

    def process_response(self, request, response):
        if response.status_code != 404:
            return response

        try:
            return read(request, request.path_info)
        except Http404:
            return response
        except:
            if settings.DEBUG:
                raise
            return response
