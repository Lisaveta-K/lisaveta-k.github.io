# -*- coding: utf-8 -*-

import os.path

from fabric.api import env, run, sudo, execute


# Путь до кода проекта
PROJECT_ROOT = '/var/www/tomat/app'

MANAGE_PY_PATH = os.path.join(PROJECT_ROOT, 'manage.py')

PYTHON_PATH = os.path.join(PROJECT_ROOT, '.env/bin/python')

PIP_PATH = os.path.join(PROJECT_ROOT, '.env/bin/pip')

# Файл, на который нужно делать `touch` для рестарта uwsgi
UWSGI_TOUCH_FILE = '/etc/uwsgi/uwsgi.d/tomat.ini'

env.hosts = ('tomat-podarky.ru', )


def deploy():
    execute(pre_clean)
    execute(checkout)
    execute(migrate)
    execute(static_compile)
    execute(static_collect)
    execute(app_restart)
    execute(cache_flush)
    execute(post_process)


def pre_clean():
    sudo('rm -rf %s/*' % os.path.join(PROJECT_ROOT, 'static', 'css', 'compiled'))


def checkout():
    """Обновление кода"""

    sudo('cd %s; git pull' % PROJECT_ROOT)


def migrate():
    sudo('%(python)s %(manage)s migrate' % {
        'python': PYTHON_PATH,
        'manage': MANAGE_PY_PATH,
    })


def static_compile():

    css_files = [
        ('static/less/scout.less', 'static/css/compiled/scout.css'),
        ('static/less/print.less', 'static/css/compiled/print.css'),
    ]

    for less_filename, css_filename in css_files:
        bits = (
            'lessc',
            '-x',  # compress
            '-O2',  # optimize
            '-s',  # silent
            os.path.join(PROJECT_ROOT, less_filename),
            os.path.join(PROJECT_ROOT, css_filename),
            )
        sudo(' '.join(bits))

    js_root = os.path.join(PROJECT_ROOT, 'static', 'js', 'lib')
    required_files = (
        'jquery-1.10.0.min.js',
        'bootstrap.3.0.0.min.js',
        'flight.1.1.0.min.js',
        'jquery.cookie.1.3.1.min.js',
        'jquery.equalheightcolumns.1.1.js',
        'jquery.menu-aim.min.js',
        'nprogress.0.1.2.min.js',
        'typeahead.0.9.3.min.js',
        'hogan-2.0.0.min.js',
        'flying-focus.1.3.0.min.js',
    )

    result_filename = os.path.join(js_root, 'mashup.js')
    sudo('touch %s' % result_filename)
    sudo('truncate --size 0 %s' % result_filename)
    for filename in required_files:
        sudo('cat %s >> %s' % (os.path.join(js_root, filename), result_filename))
        # sudo('''echo -e '\\n' >> %s''' % (os.path.join(js_root, filename), result_filename))

def static_collect():
    """Выкладка статики"""

    sudo('%(python)s %(manage)s collectstatic --noinput --clear -v 0' % {
        'python': PYTHON_PATH,
        'manage': MANAGE_PY_PATH,
    })




def app_restart():
    """Перезагрузка приложения"""

    sudo('touch %s' % UWSGI_TOUCH_FILE)


def cache_flush():
    """Сброс кэша"""

    run('echo "flush_all" | nc 127.0.0.1 11211', timeout=1, warn_only=True)


def post_process():
    sudo('cp /var/www/tomat/app/static/css/compiled/* /var/www/tomat/www/static/css/compiled')
