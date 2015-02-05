# -*- coding: utf-8 -*-

from django.contrib import admin

from news.models import News
from news.forms import NewsAdminForm


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_visible', 'date_published')
    date_hierarchy = 'date_published'
    form = NewsAdminForm

admin.site.register(News, NewsAdmin)
