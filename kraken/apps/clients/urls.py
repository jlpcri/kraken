from django.conf.urls import patterns, url

urlpatterns = patterns('kraken.apps.clients.views',
                       url(r'^clients/$', 'clients', name='clients'),
                       )