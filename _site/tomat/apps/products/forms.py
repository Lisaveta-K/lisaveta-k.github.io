# -*- coding: utf-8 -*-

from xml.dom.minidom import parse

from django import forms
from pytils.translit import slugify
from annoying.decorators import autostrip
from mptt.fields import TreeNodeChoiceField

from products.models import Category, Product, Photo
from products.fields import CategorySelect2MultipleField
from utils.forms.widgets import AdminImagePreviewWidget, DimensionsWidget, RedactorWidget


@autostrip
class CategoryAdminForm(forms.ModelForm):
    """Форма категории для админки"""

    parent = TreeNodeChoiceField(queryset=Category.objects.filter(level__in=[0, 1]), required=False,
        label=u'Родительская категория')
    slug = forms.SlugField(required=False, label=u'Алиас',
        help_text=u'Используется в ссылках (если оставить поле пустым, создастся автоматически)')
    cover = forms.ImageField(label=u'Изображение', widget=AdminImagePreviewWidget, required=False)  # TODO: указать размеры изображения
    description = forms.CharField(label=u'Описание', widget=RedactorWidget, required=False)

    class Meta:
        model = Category
        fields = ('parent', 'title', 'slug', 'cover', 'description', 'is_complementary', 'is_standalone',
            'is_visible', 'show_cover_in_menu', 'position', 'complementary_cover', 'complementary_hover_cover',
            'is_signable')

    def clean(self):
        data = self.cleaned_data

        slug = data.get('slug')
        if not slug:
            data['slug'] = slugify(data['title']).strip('-')

        cover = data.get('cover')
        parent = data.get('parent')
        if not parent and not cover:
            raise forms.ValidationError(u'Нужно загрузить изображение')
        elif parent and parent.level != 0 and not cover:  # Для категорий 1 уровня изображение не нужно
            raise forms.ValidationError(u'Нужно загрузить изображение')

        return data


@autostrip
class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label=u'Описание', widget=RedactorWidget, required=False)
    dimensions = forms.CharField(label=u'Размеры', widget=DimensionsWidget,
        help_text=u'Ширина, длина, высота (см.)', required=False)
    categories = CategorySelect2MultipleField(label=u'Категории')

    class Meta:
        model = Product


class PhotoInlineAdminForm(forms.ModelForm):
    image = forms.ImageField(widget=AdminImagePreviewWidget)

    class Meta:
        model = Photo


class UploadAdminForm(forms.Form):
    """Форма загрузки файла из 1С для обновления данных по товарам"""

    file = forms.FileField(u'Файл из 1С')
    type = forms.ChoiceField(choices=(
        (1, u'Розница'),
        (2, u'Опт'),
        (3, u'Франшиза'),
    ), initial=1)
