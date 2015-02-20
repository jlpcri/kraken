from django.conf.urls import patterns, url

from kraken.apps.schemas import views

urlpatterns = patterns('kraken.apps.schemas.views',
                       url(r'^clients/(?P<client_id>\d+)/schemas/create/$', 'create_schema', name='create_schema'),
                       url(r'^clients/(?P<client_id>\d+)/schemas/(?P<schema_id>\d+)/versions/create/$', 'create_version', name='create_version'),
                       url(r'^clients/(?P<client_id>\d+)/schemas/(?P<schema_id>\d+)/versions/(?P<version_id>\d+)/edit/$', 'edit_version', name='edit_version'),
                       url(r'^clients/(?P<client_id>\d+)/schemas/(?P<schema_id>\d+)/versions/(?P<version_id>\d+)/files/create/$', 'create_file', name='create_file'),
                       url(r'^clients/(?P<client_id>\d+)/schemas/(?P<schema_id>\d+)/versions/(?P<version_id>\d+)/files/save/$', 'save_file', name='save_file'),
                       url(r'^clients/(?P<client_id>\d+)/schemas/(?P<schema_id>\d+)/versions/(?P<version_id>\d+)/files/(?P<file_id>\d+)/download/$', 'download_file', name='download_file'),
                       url(r'^clients/(?P<client_id>\d+)/schemas/(?P<schema_id>\d+)/versions/(?P<version_id>\d+)/files/(?P<file_id>\d+)/edit/$', 'edit_file', name='edit_file'),

                       url(r'^clients_list/$', views.clients_list, name='clients_list'),
                       url(r'^client/(?P<client_name>\w+)/schemas/$', views.client_schemas_list, name='client_schemas_list'),
                       url(r'^client/(?P<client_name>\w+)/schema/(?P<schema_name>\w+)/versions/$', views.schema_versions_list, name='schema_versions_list'),
                       url(r'^schemas/batch_files/$', 'batch_files', name='batch_files'),

                       )
