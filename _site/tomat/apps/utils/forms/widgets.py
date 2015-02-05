# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.forms.widgets import Textarea, MultiWidget, TextInput
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.contrib.gis.geos import fromstr
from easy_thumbnails.files import get_thumbnailer

from utils.exceptions import handle_exception


class AdminImagePreviewWidget(AdminFileWidget):

    def render(self, name, value, attrs=None):
        output = []

        if value:
            try:
                thumb = get_thumbnailer(value)['preview']
            except:
                handle_exception()
            else:
                html = '<img src="%s" alt="">' % thumb.url
                output.append(html)

        output.append(super(AdminImagePreviewWidget, self).render(name, value, attrs))

        return mark_safe(u''.join(output))


class RedactorWidget(Textarea):

    HTML = '''<script type="text/javascript">
        (function($) {
            $('#%(id)s').redactor({
                lang: 'ru',
                imageUpload: '%(image_upload)s',
                fileUpload: '%(file_upload)s'
            });
        })(django.jQuery);
    </script>
    <style type="text/css">
        .redactor_box {
            width: 800px;
            margin-left: 104px;
            min-height: 600px;
        }
        .redactor_editor p {
            margin-left: 10px !important;
            padding-left: 0 !important;
        }
        .redactor_editor ul {
            margin-left: 0 !important;
        }
    </style>
    '''

    class Media:
        css = {
            'all': (
                '/static/css/redactor.css',
            )
        }
        js = (
            '/static/js/jquery.admin-compat.js',
            '/static/js/lib/redactor.js',
            '/static/js/lib/redactor-ru.js',
        )

    def render(self, name, value, attrs=None):
        html = super(RedactorWidget, self).render(name, value, attrs)

        script = self.HTML % {
            'id': attrs['id'],
            'image_upload': reverse('uploads.views.upload_image'),
            'file_upload': reverse('uploads.views.upload_file'),
        }

        return mark_safe(html + script)


class DimensionsWidget(MultiWidget):

    DELIMITER = u'×'

    def __init__(self, attrs=None):
        widgets = (
            TextInput(attrs=attrs),
            TextInput(attrs=attrs),
            TextInput(attrs=attrs),
        )

        super(DimensionsWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        bits = (value or '').split(self.DELIMITER)
        if len(bits) != 3:
            return ()

        return bits

    def value_from_datadict(self, data, files, name):
        value = super(DimensionsWidget, self).value_from_datadict(data, files, name)
        if not any(value):
            return u''

        return self.DELIMITER.join(value)


class PointWidget(TextInput):

    class Media:
        js = (
            'http://maps.api.2gis.ru/1.0',
        )

    def render(self, name, value, attrs=None):
        context = {
            'name': name,
            'value': value,
            'id': attrs['id'],
        }

        return render_to_string('forms/widgets/point_widget.html', context)

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        if value:
            return fromstr(value, srid=4326)
