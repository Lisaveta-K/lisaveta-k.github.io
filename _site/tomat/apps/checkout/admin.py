# -*- coding: utf-8 -*-
import datetime

from django.contrib import admin
from django.utils.html import linebreaks

from checkout.models import Order, OrderItem
from users.heplers import combine_date_and_time
from users.models import User


class TypeFilter(admin.SimpleListFilter):

    title = u'Тип заказа'
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('retail', u'Розничные'),
            ('wholesale', u'Оптовые'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'retail':
            return queryset.filter(user__status__in=(User.STATUS_ADMIN, User.STATUS_CUSTOMER))
        elif self.value() == 'wholesale':
            return queryset.filter(user__status__in=(User.STATUS_FRANCHISEE, User.STATUS_WHOLESALE))
        return queryset


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = readonly_fields = ('product', '_sign', 'per_item', '_sku', 'amount')
    extra = 0

    def _sku(self, obj):
        return obj.product.sku
    _sku.short_description = u'Артикул'

    def _sign(self, obj):
        return linebreaks(obj.sign)
    _sign.short_description = u'Подпись'
    _sign.allow_tags = True


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'net', '_status', '_payment_type', 'delivery', '_delivery_datetime', 'created')
    list_select_related = True
    list_filter = (TypeFilter, 'status', 'payment_type', 'delivery')
    date_hierarchy = 'created'
    inlines = (OrderItemInline, )
    readonly_fields = ('address', '_delivery_datetime', '_receiver_title', '_phone', '_receiver_phone', '_receiver_email', 'shop', 'status', 'user',
        'net', 'code', 'delivery_cost', 'comment', 'created', 'delivery', 'payment_type')

    def _delivery_datetime(self, obj):
        return combine_date_and_time(obj.delivery_date, obj.delivery_time)
    _delivery_datetime.short_description = u'Дата и время доставки'

    def _status(self, obj):
        return obj.get_status_display()
    _status.short_description = u'Статус'

    def _payment_type(self, obj):
        return obj.get_payment_type_display()
    _payment_type.short_description = u'Оплата'

    def _receiver_title(self, obj):
        return obj.address.receiver_title
    _receiver_title.short_description = u'Получатель'

    def _phone(self, obj):
        return obj.address.phone
    _phone.short_description = u'Телефон'

    def _receiver_email(self, obj):
        return obj.address.email
    _receiver_email.short_description = u'E-mail получателя'

    def _receiver_phone(self, obj):
        return obj.address.receiver_phone
    _receiver_phone.short_description = u'Телефон получателя'

admin.site.register(Order, OrderAdmin)
