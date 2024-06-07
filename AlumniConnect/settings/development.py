from AlumniConnect.settings.common import *

SECRET_KEY = "dikj)qxgkhe7v$y7l))d!!nkut&^6q7+x^@ys7c1z!#!&*94r5"

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = "Alumni Cell IIITDMJ <your-email@gmail.com>"
BCC_EMAILS = ["bcc-email1@gmail.com", "bcc-email2@gmail.com"]

if DEBUG:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, '..', 'static/'),)

    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    INTERNAL_IPS = ('127.0.0.1',)
