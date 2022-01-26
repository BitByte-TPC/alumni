import ast

from AlumniConnect.settings.common import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY_ALUMNI")

DEBUG = False

ALLOWED_HOSTS = ast.literal_eval(os.environ.get("ALLOWED_HOSTS"))

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))

DEFAULT_FROM_EMAIL = os.environ.get("SENDER_EMAIL")
BCC_EMAILS = ast.literal_eval(os.environ.get("BCC_EMAILS"))


STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static/')
