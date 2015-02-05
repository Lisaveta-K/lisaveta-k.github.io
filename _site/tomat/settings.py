# -*- coding: utf-8 -*-

import os.path

from django.core.urlresolvers import reverse_lazy
from easy_thumbnails.conf import Settings as easy_thumbnails_defaults


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = (
    ('', 'leal_26@mail.ru'),
    ('', 'tomat_3@mail.ru'),
    ('', 'tomat_buyer@mail.ru'),
    (u'Ирина Ершова', 'rina.tomat@gmail.com'),
    (u'Татьяна Люжей', 'luget2002@mail.ru'),
    ('SvartalF', 'self@svartalf.info'),
    ('yES', 'semiguzov@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Irkutsk'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru_RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'utils.storage.LessFileSystemFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'utils.context_processors.settings',
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'utils.breadcrumbs.middleware.BreadcrumbsMiddleware',
    'cart.middleware.CartMiddleware',
    'pages.middleware.PageFallbackMiddleware',
    'utils.middleware.OperaNumeroSignFixMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.sitemaps',

    'easy_thumbnails',
    'mptt',
    'pytils',
    'django_select2',
    'south',
    'robokassa',
    'utils',
    'captcha',
    'bootstrap3_datetime',

    'products',
    'cart',
    'checkout',
    'home',
    'shops',
    'news',
    'adverts',
    'ideas',
    'users',
    'pages',
)

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = reverse_lazy('users.auth.login')

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s:%(funcName)s:%(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    }
}

THUMBNAIL_ALIASES = {
    'products': {
        'small': {
            'size': (40, 40),
            'crop': True,
        },
        'preview': {
            'size': (100, 100),
            'crop': True,
        },
        'cover': {
            'size': (160, 160),
            'crop': True,
        },
        'image': {
            'size': (386, 290),
            'crop': False,
        },
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',  # Для старых логинов
)

LESS_OUTPUT_DIRECTORY = os.path.join(PROJECT_PATH, 'static', 'css', 'compiled')

LESS_COMPILER = 'lessc'

ROBOKASSA_LOGIN = 'test'
ROBOKASSA_PASSWORD1 = 'test'

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER = 'order@tomat-podarky.ru'
EMAIL_FROM = u'Интернет-магазин «Томат» <order@tomat-podarky.ru>'
EMAIL_SUBJECT_PREFIX = ''

# Публичный URL для raven, на который будут отправляться ошибки от raven-js
RAVEN_PUBLIC_URI = ''

GOOGLE_ANALYTICS_ID = ''
YANDEX_METRIKA_ID = 0
VK_API_ID = 0
FACEBOOK_API_ID = 0

THUMBNAIL_PROCESSORS = easy_thumbnails_defaults.THUMBNAIL_PROCESSORS + (
    'utils.thumbnail.processors.watermark_processor',
)

SOUTH_MIGRATION_MODULES = {
    'captcha': 'captcha.south_migrations',
}

from settings_local import *
