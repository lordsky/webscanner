"""
Django settings for webscanner project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from kombu import Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ef7_65ra!(t6^*^mku$(by28b@oc)n*j!i(&6%8daernmp^5pp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '10.127.21.237', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'scanner',
    # 'kombu.transport.django',
    # 'djcelery',
]

#MIDDLEWARE = [
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webscanner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'webscanner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'webscanner',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            "init_command": "SET GLOBAL max_connections = 100000", #<-- The fix
         }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# Login redirect url
LOGIN_REDIRECT_URL = '/'



# celery settings
# celery broker
CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'

# celery result backend
# CELERY_RESULT_BACKEND = 'redis://localhost/0'

# celery meseage format
CELERY_ACCEPT_CONTENT = ['application/json',]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

#celery timezone
CELERY_TIMEZONE = TIME_ZONE


# default_exchange = Exchange('default', type='direct')
# priority_exchange = Exchange('ipscan', type='direct')
# set celery default queue
# task_default_queue
CELERY_TASK_DEFAULT_QUEUE = "default"
# CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
# set celery queues
CELERY_QUEUES = (    #set queue, bind routing_key
    Queue('ipscan', routing_key='ipscan.#'),
    Queue('default', binding_key='default'),
    Queue('ipscanmanager', routing_key='ipscanmanager.#'),
    # Queue('vulnscan', routing_key='vulnscan'),
)


CELERY_TASK_ROUTES = ({  #put task into queue and bind the routing_key
    'scanner.tasks.task_masscan': {
        'queue': 'ipscan',
        'routing_key': 'ipscan.masscan',
    },
    'scanner.tasks.nmap_scan': {
        'queue': 'ipscan',
        'routing_key': 'ipscan.nmap',
    },
    'scanner.tasks.nmap_scan2': {
        'queue': 'ipscanmanager',
        'routing_key': 'ipscanmanager.nmap2',
    },
    'scanner.tasks.nmap_scan3': {
        'queue': 'ipscanmanager',
        'routing_key': 'ipscanmanager.nmap3',
    }
})
