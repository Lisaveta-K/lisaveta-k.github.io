# -*- coding: utf-8 -*-

import re
import json
import os.path
import urllib2
import datetime
import uuid
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management import BaseCommand

from news.models import News


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = args[0]

        if path.startswith('http'):
            content = json.load(urllib2.urlopen(path))
        else:
            content = json.load(open(path))

        for entry in content:
            try:
                news = News.objects.get(id=int(entry['id']))
            except News.DoesNotExist:
                news = News(id=int(entry['id']))

            if not 'html' in entry or entry['pub'] == '0':
                continue

            news.title = entry['name']
            news.caption = entry['announce']
            news.is_visible = entry['pub'] == '10'
            news.date_published = datetime.datetime.strptime(entry['time'], '%d.%m.%Y').date()
            news.content = entry['html']
            news.save()

            for url_hash in re.findall('src="/pic/(.*?)/"', news.content):
                url = 'http://tomat-podarky.ru/pic/%s/' % url_hash

                fp = ContentFile(requests.get(url).content)
                today = datetime.date.today()
                target_name = 'uploads/%(year)d/%(month)d/%(name)s%(ext)s' % {
                    'year': today.year,
                    'month': today.month,
                    'name': uuid.uuid4().hex,
                    'ext': '.jpg',
                }
                filepath = os.path.join(settings.MEDIA_ROOT, target_name)
                out = open(filepath, 'w')
                out.write(fp.read())
                out.close()

                news.content = news.content.replace('/pic/%s/' % url_hash, '/media/%s' % target_name)
            news.save()
