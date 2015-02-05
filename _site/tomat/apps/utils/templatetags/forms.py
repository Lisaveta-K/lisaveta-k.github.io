# -*- coding: utf-8 -*-

from django import template
from django.template import RequestContext
from django.template.base import parse_bits
from django.template.loader import render_to_string


register = template.Library()


class FormNode(template.Node):

    default_kwargs = {
        'action': '.',
        'method': 'POST',
        'label': u'Сохранить',
    }

    def __init__(self, forms, kwargs):
        self.forms = forms
        self.kwargs = kwargs

    def render(self, context):
        kwargs = {}
        for k, v in self.kwargs.items():
            kwargs[k] = v.resolve(context)

        for k, v in self.default_kwargs.items():
            if not k in kwargs:
                kwargs[k] = v

        forms = []
        for form in self.forms:
            forms.append(form.resolve(context))

        template_context = {
            'forms': forms,
        }
        template_context.update(kwargs)

        return render_to_string('forms/form.html', template_context, RequestContext(context['request']))


@register.tag
def render_form(parser, token):

    args, kwargs = parse_bits(parser, token.split_contents()[1:], (), varargs=True, varkw=True, defaults=None,
        takes_context=False, name='render_form')

    return FormNode(args, kwargs)


@register.simple_tag
def render_field(field):
    return render_to_string('forms/form_field.html', {'field': field})
