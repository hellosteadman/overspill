from __future__ import absolute_import
from djcelery import setup_loader
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']
STATIC_URL = '/static/'

setup_loader()
