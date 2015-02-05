from django.conf.urls import patterns, url

from kraken.apps.schemas import views

urlpatterns = patterns('kraken.apps.schemas.views',
                       url(r'^schemas/$', 'schemas', name='schemas'),
                       url(r'^schemas/versions/$', 'schema_version_list', name='schema_version_list'),
                       url(r'^schemas/batch_files/$', 'batch_files', name='batch_files'),

                       url(r'^clients/(?P<client_id>\d+)/schemas/create/$', 'create_schema', name='create_schema'),
                       url(r'^schemas/versions/create/$', 'create_version', name='create_version'),
                       url(r'^schemas/files/create/$', 'create_file', name='create_file'),
                       url(r'^schemas/(?P<client_id>\d+)/save/$', 'save_schema', name='save_schema'),
                       url(r'^schemas/batch_files/$', 'batch_files', name='batch_files'),

                       url(r'^client/(?P<client_id>\d+)/schemas/$', views.client_schemas_list, name='client_schemas_list'),

                       url(r'^client/schema/versions/new/$', views.schema_version_new, name='schema_version_new'),
                       url(r'^client/schema/versions/$', views.schema_version_list, name='schema_version_list'),
                       url(r'^client/schema/version/edit/$', views.schema_version_edit, name='schema_version_edit')

                       )
