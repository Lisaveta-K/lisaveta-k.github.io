# -*- coding: utf-8 -*-

from django.contrib import admin

from ideas.models import Idea, Category
from ideas.forms import IdeaAdminForm, CategoryAdminForm


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('title', )

admin.site.register(Category, CategoryAdmin)


class IdeaAdmin(admin.ModelAdmin):
    form = IdeaAdminForm
    list_display = ('title', 'is_visible', 'created')
    list_filter = ('is_visible', )

admin.site.register(Idea, IdeaAdmin)
