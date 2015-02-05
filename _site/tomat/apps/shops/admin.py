# -*- coding: utf-8 -*-

from django.contrib import admin

from checkout.models import CourierCity
from shops.models import City, Shop, Delivery, Discount
from shops.forms import ShopAdminForm


admin.site.register(CourierCity)
admin.site.register(City)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'allow_delivery')
    form = ShopAdminForm
    list_select_related = True

admin.site.register(Shop, ShopAdmin)


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_retail', 'is_wholesale')

admin.site.register(Delivery, DeliveryAdmin)

admin.site.register(Discount)
