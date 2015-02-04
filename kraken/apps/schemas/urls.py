from django.conf.urls import patterns, url

from kraken.apps.schemas import views

urlpatterns = patterns('kraken.apps.schemas.views',
                       url(r'^schemas/$', 'schemas', name='schemas'),
                       url(r'^schemas/batch_files/$', 'batch_files', name='batch_files'),

                       url(r'^client/schemas/new/$', views.client_schema_new, name='client_schema_new'),
                       url(r'^client/(?P<client_id>\d+)/schemas/$', views.client_schemas_list, name='client_schemas_list'),

                       url(r'^client/schema/versions/new/$', views.schema_version_new, name='schema_version_new'),
                       url(r'^client/schema/versions/$', views.schema_version_list, name='schema_version_list'),
                       url(r'^client/schema/version/edit/$', views.schema_version_edit, name='schema_version_edit')

                       )
