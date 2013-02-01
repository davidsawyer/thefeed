import os, sys

sys.path.append("/home/thefeed/django_proj")
sys.path.append('/home/thefeed/django_proj/thefeed')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thefeed.settings")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
'''
from django.core.handlers.wsgi import get_wsgi_application
application = get_wsgi_application()
'''

'''
import os
import os.path
import sys

#sys.path.append("/home/thefeed/django_proj")
sys.path.append("/home/thefeed/django_proj/thefeed")

os.environ["DJANGO_SETTINGS_MODULE"] = "thefeed.settings"

# This application object is used by the development server
# as well as any WSGI server configured to use this file.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
'''
