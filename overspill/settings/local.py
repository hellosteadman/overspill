from __future__ import absolute_import
import os
from djcelery import setup_loader
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_ROOT = os.getenv('STATIC_ROOT')
MEDIA_ROOT = os.getenv('MEDIA_ROOT')
STATIC_URL = '/static/'

CELERY_REDIRECT_STDOUTS = False
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

setup_loader()
