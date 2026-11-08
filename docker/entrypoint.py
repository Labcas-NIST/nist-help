# encoding: utf-8

'''Docker entrypoint for Gunicorn's WSGI server.'''

from django.core.wsgi import get_wsgi_application
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nisthelp.settings.production')
os.environ.setdefault('SECURE_COOKIES', 'True')
os.environ.setdefault('STATIC_ROOT', '/app/static')
os.environ.setdefault('MEDIA_ROOT', '/app/media')

application = get_wsgi_application()
