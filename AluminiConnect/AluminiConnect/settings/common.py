"""
Django settings for AluminiConnect project.
"""

import os

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
    'applications.members',
    'applications.news',
    'applications.geolocation',
    'applications.publications',
    'applications.gallery',
    'applications.chapter',
    'ckeditor',
    'ckeditor_uploader',
    'tempus_dominus'
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

ROOT_URLCONF = 'AluminiConnect.urls'

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

WSGI_APPLICATION = 'AluminiConnect.wsgi.application'

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

EMAIL_USE_TLS = True
# EMAIL_HOST = 'in-v3.mailjet.com'
# EMAIL_HOST_USER = 'Student Alumni Cell (SAC), IIITDMJ'
# EMAIL_HOST_PASSWORD = os.environ.get('PASSWD')
EMAIL_PORT = 587

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# CELERY STUFF
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
PASSWORD_RESET_TIMEOUT_DAYS = 1
ANYMAIL = {
    # (exact settings here depend on your ESP...)
    "MAILJET_API_KEY": os.environ.get("MJ_APIKEY_PUBLIC", ""),
    "MAILJET_SECRET_KEY": os.environ.get("MJ_APIKEY_PRIVATE", ""),  # your Mailgun domain, if needed

}
MAILJET_API_URL = "https://api.mailjet.com/v3.1"
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"  # or sendgrid.EmailBackend, or...
DEFAULT_FROM_EMAIL = "Student Alumni Cell IIITDMJ <alumni@iiitdmj.ac.in>"  # if you don't already have this in settings
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
