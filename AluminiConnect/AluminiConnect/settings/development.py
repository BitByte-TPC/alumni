from AluminiConnect.settings.common import *

SECRET_KEY = "dikj)qxgkhe7v$y7l))d!!nkut&^6q7+x^@ys7c1z!#!&*94r5"

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

if DEBUG:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, '..', 'static/'),)

    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1',)
