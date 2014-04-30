# coding=utf-8
"""
Django settings for cunuc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext as _
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f1myj!61hh!(m(j5+mx@@mst3l#p*ni_dbou54co2_31*5o9j!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'hackusername',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cunuc.urls'

WSGI_APPLICATION = 'cunuc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

#agregado por martin munoz
AUTH_USER_MODEL = 'hackusername.MyUser'


TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), '../templates').replace('\\', '/')
)

#TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",)

LOGIN_URL = '/login/'

#AUTHENTICATION_BACKENDS = ('hackusername.models.MyBackend',)

if DEBUG:
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'martin@cursostotales.com'
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'testing@example.com'

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), '../locale').replace('\\', '/'),
)

STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__), "../static").replace('\\', '/'),
)

FACEBOOK_APP_ID = 'YOUR FACEBOOK APP ID'
FACEBOOK_APP_SECRET = 'YOUR FACEBOOK APP SECRET'
LINKEDIN_APP_ID = 'YOUR LINKEDIN APP ID'
LINKEDIN_APP_SECRET = 'YOUR LINKEDIN APP SECRET'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'hackusername.models.MyFacebookBackend',
    'hackusername.models.MyLinkedinBackend',
)