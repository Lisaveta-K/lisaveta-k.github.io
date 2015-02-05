# -*- coding: utf-8 -*-

from django.conf import settings as global_settings


def settings(request):
    return {
        'settings': global_settings,
    }
