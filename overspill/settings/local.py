from __future__ import absolute_import
from djcelery import setup_loader
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_URL = '/static/'

CELERY_REDIRECT_STDOUTS = False
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

setup_loader()
