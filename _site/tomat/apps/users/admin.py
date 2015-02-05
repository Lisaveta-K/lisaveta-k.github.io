# -*- coding: utf-8 -*-

from django.contrib import admin

from users.models import User, Address, Company
from users.forms import UserAdminForm


class CompanyInline(admin.StackedInline):
    model = Company
    max_num = 1
    extra = 0


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    inlines = (CompanyInline, AddressInline)
    list_display = ('email', 'title', 'phone', 'created', '_status')
    list_filter = ('status',)
    search_fields = ('email', 'title')

    def _status(self, obj):
        return obj.get_status_display()
    _status.short_description = u'тип'

    def save_model(self, request, obj, form, change):
        obj.is_active = obj.status == User.STATUS_ADMIN
        obj.save()

admin.site.register(User, UserAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('original_string', 'is_active', 'postal_code', 'city', 'street', 'house', 'flat')
    list_editable = ('postal_code', 'city', 'street', 'house', 'flat')
    list_select_related = True

    def is_active(self, obj):
        return obj.user.is_active
    is_active.short_description = u'А'
    is_active.boolean = True

admin.site.register(Address, AddressAdmin)
