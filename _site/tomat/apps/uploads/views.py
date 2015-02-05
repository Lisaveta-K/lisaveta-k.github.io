# -*- coding: utf-8 -*-

import datetime
import uuid
import os.path

from django.http import HttpResponseForbidden, HttpResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from pytils.translit import slugify

from uploads.forms import ImageForm, FileForm
from utils.http import JsonResponse


# TODO: require_POST декоратор
# TODO: запрос должен быть доступен только админам
@csrf_exempt
def upload_image(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.cleaned_data['file']

        today = datetime.date.today()
        target_name = 'uploads/%(year)d/%(month)d/%(name)s%(ext)s' % {
            'year': today.year,
            'month': today.month,
            'name': uuid.uuid4().hex,
            'ext': os.path.splitext(image.name)[1],
        }

        image_path = default_storage.save(target_name, image)
        url = default_storage.url(image_path)

        return JsonResponse({  # TODO: использовать JsonResponse
            'filelink': url,
        })

    return HttpResponseForbidden()


# TODO: require_POST декоратор
# TODO: запрос должен быть доступен только админам
@csrf_exempt
def upload_file(request):
    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.cleaned_data['file']
        name, ext = os.path.splitext(image.name)
        name = slugify(name)

        today = datetime.date.today()
        target_name = 'uploads/%(year)d/%(month)d/%(name)s%(ext)s' % {
            'year': today.year,
            'month': today.month,
            'name': name,
            'ext': ext,
        }

        image_path = default_storage.save(target_name, image)
        url = default_storage.url(image_path)

        return JsonResponse({  # TODO: использовать JsonResponse
            'filelink': url,
            'filename': os.path.basename(image_path),
        })

    return HttpResponseForbidden()
