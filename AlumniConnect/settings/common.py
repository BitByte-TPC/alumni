"""
Django settings for AlumniConnect project.
"""

import os
from pathlib import Path
import logging.config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = [
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
    'anymail',
    'easy_thumbnails',
    'imagekit',
    'crispy_forms',
    'applications.alumniprofile',
    'applications.awards',
    'applications.blog',
    'applications.events_news',
    'applications.job_posting',
    'applications.adminportal',
    'applications.members',
    'applications.news',
    'applications.geolocation',
    'applications.publications',
    'applications.gallery',
    'applications.chapter',
    'ckeditor',
    'ckeditor_uploader',
    'tempus_dominus',
    'AlumniConnect',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AlumniConnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['/', os.path.join(BASE_DIR, '..', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AlumniConnect.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '..', 'db.sqlite3'),
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media/')
MEDIA_URL = '/media/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
        'extraplugins': ['table'],
        'width': '100%'
    }
}

TEMPUS_DOMINUS_LOCALIZE = True

# CELERY STUFF
CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

PASSWORD_RESET_TIMEOUT_DAYS = 1
ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILJET_API_KEY": os.environ.get("MJ_APIKEY_PUBLIC", ""),
    "MAILJET_SECRET_KEY": os.environ.get("MJ_APIKEY_PRIVATE", ""),  # your Mailgun domain, if needed

}
MAILJET_API_URL = "https://api.mailjet.com/v3.1"
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"  # or sendgrid.EmailBackend, or...
DEFAULT_FROM_EMAIL = "Alumni Cell IIITDMJ <alumni@iiitdmj.ac.in>"  # if you don't already have this in settings
SERVER_EMAIL = os.environ.get("MJ_SENDER_EMAIL", "")  # ditto (default from-email for Django errors)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class Filter(logging.Filter):
    def __init__(self, level):
        self.level = level
        super().__init__()

    def filter(self, record):
        return record.levelno == self.level

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'detailed': {
            'format': (
                'Level - {levelname}\n'
                'Time - {asctime}\n'
                'Module - {module}\n'
                'PID - {process:d}\n'
                'TID - {thread:d}\n'
                'Message - {message}\n'
                '\n'
            ),
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'warning_filter': {
            '()': Filter,
            'level': logging.WARNING,
        },
        'error_filter': {
            '()': Filter,
            'level': logging.ERROR,
        },
        'critical_filter': {
            '()': Filter,
            'level': logging.CRITICAL,
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename': os.path.join(LOG_DIR, 'warning.log'),
            'filters': ['warning_filter'],
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'filters': ['error_filter'],
        },
        'critical_file': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'formatter': 'detailed',
            'filename': os.path.join(LOG_DIR, 'critical.log'),
            'filters': ['critical_filter'],
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'] if os.getenv('DJANGO_ENV') == 'development' else ['warning_file', 'error_file', 'critical_file'],
            'level': 'INFO' if os.getenv('DJANGO_ENV') == 'development' else 'WARNING',
            'propagate': True,
        },
    },
}

