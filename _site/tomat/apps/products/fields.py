# -*- coding: utf-8 -*-

from django_select2.fields import AutoModelSelect2MultipleField

from products.models import Product, Category


class CategorySelect2MultipleField(AutoModelSelect2MultipleField):
    queryset = Category.objects
    search_fields = ('title__icontains', )


class ProductSelect2MultipleField(AutoModelSelect2MultipleField):
    queryset = Product.objects.filter(is_visible=True, categories__isnull=False).distinct()
    search_fields = ('title__icontains', )

    def label_from_instance(self, obj):
        return u'#{} ({})'.format(obj.title, obj.sku)
