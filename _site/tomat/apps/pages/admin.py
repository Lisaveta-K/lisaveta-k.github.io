# -*- coding: utf-8 -*-

from django.contrib import admin

from pages.models import Page
from pages.forms import PageAdminForm


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    form = PageAdminForm

admin.site.register(Page, PageAdmin)
