# encoding: utf-8


from .base import *  # noqa: F401, F403
import os

DEBUG = False
FORCE_SCRIPT_NAME = '/nist/help'
WAGTAIL_GRAVATAR_PROVIDER_URL = None
STATIC_ROOT = '/home/ddsaops/nist-help/static'
MEDIA_ROOT = '/home/ddsaops/nist-help/media'


# Secret Key
# ----------
#
# Used to sign sessions, etc. In production this comes from the environment and presumably
# Docker sets it. If it's not set, the default is to use `None`, which'll make Django abort,
# which is what we want, because this absolutely has to be set!
#
# 🔗 https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SECRET_KEY

SECRET_KEY = os.getenv('SECRET_KEY')
if SECRET_KEY is None:
    raise ValueError('🚨 In operations, the SECRET_KEY variable cannot be unset')


# Handling of Session Keys
# ------------------------
#
# In production, we want cookies to be sent securely and only over HTTP (sorry JavaScript)—and
# similarly for CSRF cookies.
#
# 🔗 https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-secure
# 🔗 https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-SESSION_COOKIE_HTTPONLY
# 🔗 https://docs.djangoproject.com/en/3.2/ref/settings/#csrf-cookie-secure
# 🔗 https://docs.djangoproject.com/en/3.2/ref/settings/#csrf-cookie-httponly

_secure = os.getenv('SECURE_COOKIES', 'True') == 'True'
SESSION_COOKIE_SECURE = SESSION_COOKIE_HTTPONLY = CSRF_COOKIE_SECURE = CSRF_COOKIE_HTTPONLY = _secure
del _secure


# Allowed Hosts
# -------------
#
# Valid `Host:` headers that we'll serve
#
# 🔗 https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-ALLOWED_HOSTS
# 🔗 https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-USE_X_FORWARDED_HOST

ALLOWED_HOSTS = [i.strip() for i in os.getenv('ALLOWED_HOSTS', '.jpl.nasa.gov').split(',')]
USE_X_FORWARDED_HOST = True


# Logging
# -------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%b-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/tmp/nisthelp.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
        'root': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
}
