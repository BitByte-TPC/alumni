from AluminiConnect.settings.common import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY_ALUMNI")

DEBUG = False

ALLOWED_HOSTS = ['58.84.25.100', '103.59.142.75', 'https://www.iiitdmj.ac.in/sac.iiitdmj.ac.in/', 'sac.iiitdmj.ac.in']

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.environ.get("EMAIL_PORT", cast=int)

DEFAULT_FROM_EMAIL = os.environ.get("SENDER_EMAIL")
BCC_EMAIL_ID = os.environ.get("BCC_EMAIL_ID")


STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static/')
