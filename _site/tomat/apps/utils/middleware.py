# -*- coding: utf-8 -*-

class OperaNumeroSignFixMiddleware(object):
    """Opera 12.16 (возможно и другие версии) под Windows
    неправильно отображает знак №, рендеря его другим шрифтом.

    Глупое, но работающее решение - заменять этот символ на HTML entity,
    тогда опера рендерит его правильно"""

    def process_response(self, request, response):
        if response.streaming or response.get('Content-Type') != 'text/html' or response.status_code in (500, ):
            return response

        try:
            response.content = response.content.replace(u'№', u'&#8470;')
        except UnicodeDecodeError:
            pass
        return response
