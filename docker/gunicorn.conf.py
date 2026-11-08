# flake8: noqa

wsgi_app = 'entrypoint:application'
bind = ['0.0.0.0:8000']
preload_app = True
daemon = False

accesslog = '-'
errorlog = '-'
loglevel = 'info'
