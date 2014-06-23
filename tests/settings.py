"""
Django settings for oscar_impersonate/tests project.
"""

DEBUG = True

SECRET_KEY = 'x1l-2%yjehl&coha1e@bve%zb86phjeke!pnq+0pvg*miijunp'

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'oscar_impersonate.middleware.ImpersonateMiddleware',
]

ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'impersonate',
)

from oscar_impersonate import OSCAR_IMPERSONATE_TEMPLATE_DIR
TEMPLATE_DIRS = (
    OSCAR_IMPERSONATE_TEMPLATE_DIR,
)
