from base import *

DEBUG = True

TEMPLATE_DEBUG = DEBUG

if socket.gethostname() == 'sliu-OptiPlex-GX520':  # desktop
    #STATIC_URL = 'http://apps.qaci01.wic.west.com/static/'
    STATICFILES_DIRS = ('/opt/static/',)
elif socket.gethostname() == 'OM1960L1':
    #STATIC_ROOT = '/static/'
    STATICFILES_DIRS = ('C:/Users/sliu/static',)


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'kraken',
#         'USER': 'visilog',
#         'PASSWORD': '6ewuON0>;wHTe(DttOwjg#5NY)U497xKVwOxmQt60A1%}r:@qC&`7OdSP8u[.l[',
#         'HOST': 'linux6437.wic.west.com',
#         'PORT': '5432'
#     }
# }