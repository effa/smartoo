"""
Django settings for smartoo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '24o@tak8xtx)mr*@uia!_(abl5jnru(@-_u^4&t@0c$t$zy=a1'

ON_SERVER = os.getenv('ON_AL', "False") == "True"
DEBUG = os.getenv('DJANGO_DEBUG', "False") == "True"
if not ON_SERVER:
    DEBUG = True
DATABASES = {"default": dj_database_url.config(default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'))}
ALLOWED_HOSTS = ['*']

TEMPLATE_DEBUG = True

ADMINS = (('Tomas Effenberger', 'xeffenberger@gmail.com'),)

# Application definition

INSTALLED_APPS = (
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # third party
    'django_extensions',

    # my apps
    'common',
    'abstract_component',
    'knowledge',
    'exercises',
    'practice',
    'smartoo',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'smartoo.urls'

WSGI_APPLICATION = 'development.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

# we don't need timezone awereness
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

#STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
#MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
#MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'


# Global templates
#TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Sessions
#SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Caches
# TODO: use Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
        #'LOCATION': 'unique-snowflake'
    }
}


# logging

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] (%(name)s:%(lineno)d:%(funcName)s): %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'development', 'debug.log'),
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'smartoo': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'knowledge': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'exercises': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'practice': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'common': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rdflib': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
    }
}

# emails

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
SERVER_EMAIL = 'feedbackform@smartoo.thran.cz'

# ===== django_extensions settings =====

# Always use IPython for shell_plus
SHELL_PLUS = "ipython"
