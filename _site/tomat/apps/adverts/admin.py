# -*- coding: utf-8 -*-

from django.contrib import admin

from adverts.models import Promo, Coupon
from adverts.forms import PromoAdminForm, CouponAdminForm


class PromoAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_retail', 'is_wholesale', '_list_categories')
    list_filter = ('is_retail', 'is_wholesale')
    form = PromoAdminForm

    def _list_categories(self, obj):
        titles = list(obj.categories.all().values_list('title', flat=True))
        if not titles:
            return u'Главная страница'
        return u', '.join(titles)
    _list_categories.short_description = u'Категории'

admin.site.register(Promo, PromoAdmin)


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'date_start', 'date_end', 'discount_percent', 'discount_amount', 'discount_level')
    form = CouponAdminForm

    class Media:
        js = (
            '/static/js/jquery.admin-compat.js',
        )

admin.site.register(Coupon, CouponAdmin)
