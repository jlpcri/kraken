from django.conf.urls import patterns, url

urlpatterns = patterns('kraken.apps.core.views',
                       url(r'^clients/$', 'clients_list', name='clients_list'),
                       url(r'^client_schemas/$', 'client_schemas_list', name='client_schemas_list'),

                       )
