from base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

STATIC_URL = 'http://apps.qaci01.wic.west.com/static/'

DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kraken',
        'USER': 'caheyden',
    }
}