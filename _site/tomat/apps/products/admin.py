# -*- coding: utf-8 -*-

import json

from django.http import HttpResponseRedirect
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.shortcuts import render
from django.db.models import Count
from mptt.admin import MPTTModelAdmin
from pytils.numeral import get_plural
from annoying.decorators import JsonResponse
from easy_thumbnails.files import get_thumbnailer

from products.models import Category, Product, Photo
from products.forms import CategoryAdminForm, ProductAdminForm, UploadAdminForm, PhotoInlineAdminForm
from products.helpers import parse_1c


class CategoryParentFilter(SimpleListFilter):
    title = u'Категория'
    parameter_name = 'parent_id'

    def lookups(self, request, model_admin):
        return Category.objects.filter(parent__isnull=True).values_list('id', 'title')

    def queryset(self, request, queryset):
        parent_id = request.GET.get(self.parameter_name)
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)

        return queryset


class CategoryLevelFilter(SimpleListFilter):
    title = u'Уровень'
    parameter_name = 'level'

    def lookups(self, request, model_admin):
        return (
            (0, u'Первый'),
            (1, u'Второй'),
            (2, u'Третий'),
        )

    def queryset(self, request, queryset):
        value = request.GET.get(self.parameter_name)
        if value:
            queryset = queryset.filter(level=value)

        return queryset


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('title', 'parent', 'is_complementary', 'is_visible', 'products_link')
    list_select_related = True
    list_filter = (CategoryParentFilter, CategoryLevelFilter, 'is_complementary', 'is_visible')
    search_fields = ('title',)
    form = CategoryAdminForm
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'cover', 'icon', 'description'),
        }),
        (u'Свойства', {
            'fields': ('parent', 'is_visible', 'is_standalone', 'show_cover_in_menu', 'position', 'is_signable'),
        }),
        (u'Сопутствующие товары', {
            'fields': ('is_complementary', 'complementary_cover', 'complementary_hover_cover'),
        }),
    )

    def products_link(self, obj):
        if obj.level != 2:
            return ''

        url = reverse('admin:products_product_changelist')
        return u'<a href="%s?q=%s">товары</a>' % (url, obj.title)

    products_link.short_description = u'Список товаров'
    products_link.allow_tags = True

admin.site.register(Category, CategoryAdmin)


class PhotoInline(admin.TabularInline):
    model = Photo
    form = PhotoInlineAdminForm


class ProductCategoriesFilter(SimpleListFilter):
    title = u'Категории'
    parameter_name = 'categories'

    def lookups(self, request, model_admin):
        return (
            (0, u'Нет категорий'),
        )

    def queryset(self, request, queryset):
        try:
            value = int(request.GET.get(self.parameter_name))
        except (ValueError, TypeError):
            value = None
        if value == 0:
            queryset = queryset.annotate(categories_cnt=Count('categories')).filter(categories_cnt=0)

        return queryset


class QuantityFilter(SimpleListFilter):
    title = u'На складе'
    parameter_name = 'quantity'

    def lookups(self, request, model_admin):
        return (
            (0, u'Нет'),
            (1, u'Да'),
        )

    def queryset(self, request, queryset):
        try:
            value = bool(int(request.GET.get(self.parameter_name)))
        except (ValueError, TypeError):
            value = None

        kwargs = {}

        if value is True:
            kwargs['{0}__gt'.format(self.parameter_name)] = 0
        elif value is False:
            kwargs[self.parameter_name] = 0

        return queryset.filter(**kwargs)


class WholesaleQuantityFilter(QuantityFilter):
    title = u'Оптовый склад'
    parameter_name = 'wholesale_quantity'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('_preview', 'title', 'sku', 'code', 'is_visible', 'is_new', 'is_retail', 'is_wholesale', 'quantity',
                    'wholesale_quantity', '_get_categories')
    list_filter = ('is_visible', 'is_new', 'is_retail', 'is_wholesale', ProductCategoriesFilter, QuantityFilter, WholesaleQuantityFilter)
    list_display_links = ('_preview', 'title')
    search_fields = ('title', 'sku', 'code')
    inlines = (PhotoInline, )
    form = ProductAdminForm
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'sku', 'code', 'categories'),
        }),
        (u'Свойства', {
            'fields': ('is_visible', 'is_new', 'is_retail', 'is_wholesale'),
        }),
        (u'Цены', {
            'fields': ('price', 'discount', 'wholesale_price', 'wholesale_discount', 'franchisee_price', 'franchisee_discount'),
        }),
        (u'Свойства', {
            'fields': ('quantity', 'wholesale_quantity', 'weight', 'dimensions', 'pack_amount', 'box_amount'),
        }),
    )

    def _get_link(self, obj):
        return '<a href="./%d/link/">Привязка оптового товара</a>' % obj.id
    _get_link.allow_tags = True
    _get_link.short_description = u'Оптовые товары'

    def _wholesale_linked(self, obj):
        return bool(obj.wholesale_legacy_id)
    _wholesale_linked.boolean = True
    _wholesale_linked.short_description = u'Привязан оптовый товар'

    def _get_categories(self, obj):
        titles = obj.categories.values_list('title', flat=True)
        if not titles:
            return u'<Нет категорий>'
        return u', '.join(titles)
    _get_categories.short_description = u'Категории'

    def _have_categories(self, obj):
        return obj.categories.all().exists()
    _have_categories.boolean = True
    _have_categories.short_description = u'Есть категории'

    def _preview(self, obj):
        image = obj.get_main_photo()
        if not image:
            return ''
        try:
            preview = get_thumbnailer(image.image).get_thumbnail({
                'size': [80, 80],
                'crop': True,
            })
        except Exception:
            return ''

        return u'<img src="%s" alt="">' % preview.url
    _preview.short_description = u''
    _preview.allow_tags = True

    def get_urls(self):
        return patterns('',
            url(r'^upload/$', self.upload, name='products_product_upload'),
            url(r'^(?P<object_id>\d+)/link/$', self.link, name='products_product_link'),
            url(r'^link/search/$', self.link_search, name='products_product_link_search'),
        ) + super(ProductAdmin, self).get_urls()

    def upload(self, request):
        model = self.model
        opts = model._meta

        if request.POST:
            form = UploadAdminForm(request.POST, request.FILES)
            if form.is_valid():
                updated_items = 0
                type_ = int(form.cleaned_data['type'])

                price_field = {
                    1: 'price',
                    2: 'wholesale_price',
                    3: 'franchisee_price',
                }[type_]
                quantity_field = {
                    1: 'quantity',
                    2: 'wholesale_quantity',
                    3: 'wholesale_quantity',
                }[type_]

                visibility_field = 'is_retail' if price_field == 'price' else 'is_wholesale'

                for code, price, quantity in parse_1c(form.cleaned_data['file'].read()):
                    kwargs = {
                        price_field: price,
                        quantity_field: quantity,

                        # Временно убрали включение галочки
                        # visibility_field: True,

                        # Velina: когда загружаешь 1С файл, все товары, имеющие розничную и оптовую цену,
                        #   сразу автоматом попадают в эти разделы. на наборы из полирезина была установлена "левая" цена розничная,
                        #   они вообще в рознице только по 1 шт. продаваться будут, а тут целый набор за 100 р.
                        #   и вот каждый день обновляя базу цен и кол-ва на сайте я вручную убирала их из розничных товаров,
                        #   как и Снежные шары, которых вообще еще нет в наличии и предзаказ доступен только для опта
                        # Velina: а сегодня видно не успела убрать
                        # SvartalF: Так. А мы специально делали же, что все загружаемые из 1С товары сразу делаются и публикуемыми. Теперь это не надо?
                        # Velina: они публикуемыми не делаются, они просто помечаются как "Розничный товар" и "Оптовый товар",
                        #   если заполнены соотв. поля цен в файле 1С
                        # SvartalF: Да, точно
                        # SvartalF: То есть с загрузкой 1С файлов никаких проблем нет?
                        # SvartalF: Тогда как нам решить эту проблему с заказом?
                        # Velina: никак
                        # Velina: давай уберем эту автоматическую простановку галок "Розничны", "Оптовый"?
                    }
                    updated_items += Product.objects.filter(code=code).update(**kwargs)

                messages.success(request, u'В базе сайта обновлено %s' % get_plural(updated_items,
                    [u'товар', u'товара', u'товаров']))

                return HttpResponseRedirect('..')

        else:
            form = UploadAdminForm()

        context = {
            'form': form,
            'current_app': self.admin_site.name,
            'opts': opts,
            'app_label': opts.app_label,
            'object': None,
        }

        return render(request, 'admin/products/upload.html', context)

    def link(self, request, object_id):
        obj = Product.objects.get(id=object_id)
        model = self.model
        opts = model._meta

        content = json.load(open('/tmp/wholesale.json'))

        if request.POST:
            ws_id = request.POST.get('id')
            for item in content:
                if item['id'].strip() == ws_id:
                    obj.wholesale_price = float(item['unitcost'].replace(',', '.'))
                    obj.pack_amount = int(item['perpack'])
                    obj.wholesale_legacy_id = item['id'].strip()
                    obj.save()

            return HttpResponseRedirect('../..')

        code_matches = []
        article_matches = []

        for item in content:
            if obj.sku and item['article'].strip() == obj.sku:
                article_matches.append(item)
            elif obj.code and item['link'].strip() == obj.code:
                code_matches.append(item)

        context = {
            'object': obj,
            'code_matches': code_matches,
            'article_matches': article_matches,
            'current_app': self.admin_site.name,
            'opts': opts,
            'app_label': opts.app_label,
        }

        return render(request, 'admin/products/link.html', context)

    def link_search(self, request):
        query = request.GET.get('query', '').lower()
        content = json.load(open('/tmp/wholesale.json'))

        matches = []
        for item in content:
            if query in item['name'].lower():
                matches.append(item)
            elif query in item['descr'].lower():
                matches.append(item)

        return JsonResponse(matches)

    def _categories(self, obj):
        return u', '.join(obj.categories.all().values_list('title', flat=True))
    _categories.short_description = u'Категории'

admin.site.register(Product, ProductAdmin)
