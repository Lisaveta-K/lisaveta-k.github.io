# -*- coding: utf-8 -*-

from django_select2.fields import AutoModelSelect2Field

from users.models import City, Country


class CityModelSelect2Field(AutoModelSelect2Field):
    queryset = City.objects.all()
    search_fields = ('title__icontains', )
