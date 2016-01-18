from __future__ import absolute_import
from django.conf import settings

API_KEY = getattr(settings, 'CLOUDCONVERT_API_KEY')
START_PROCESS_URL = 'https://api.cloudconvert.com/process'
