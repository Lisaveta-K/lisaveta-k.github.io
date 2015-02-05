# -*- coding: utf-8 -*-

import os.path

from django.contrib.staticfiles.finders import FileSystemFinder, find
from django.contrib.staticfiles.storage import CachedStaticFilesStorage
from django.conf import settings


class LessFileSystemFinder(FileSystemFinder):

    def find(self, path, all=False):
        filename, ext = os.path.splitext(os.path.basename(path))
        if ext != '.less':
            return

        result = os.path.join(settings.LESS_OUTPUT_DIRECTORY, '%s.css' % filename)
        if os.path.exists(result):
            return result
