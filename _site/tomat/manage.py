#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.conf import settings
    from django.core.management import execute_from_command_line

    sys.path.insert(0, settings.PROJECT_PATH)
    sys.path.insert(0, os.path.join(settings.PROJECT_PATH, 'apps'))

    execute_from_command_line(sys.argv)
