from base import *

#Use QACI01 as proxy server for staging server
JIRA_PROXY = {
    'http': 'http://qaci01.wic.west.com:3128',
}

DEBUG = False

ALLOWED_HOSTS = [
    'apps.qaci01.wic.west.com',
    'apps.qaci01',
    'linux6436.wic.west.com',
    'linux6436',
    'linux6438.wic.west.com',
    'linux6438'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'kraken',
        'USER': 'visilog',
        'PASSWORD': '6ewuON0>;wHTe(DttOwjg#5NY)U497xKVwOxmQt60A1%}r:@qC&`7OdSP8u[.l[',
        'HOST': 'linux6437.wic.west.com',
        'PORT': '5432'
    }
}