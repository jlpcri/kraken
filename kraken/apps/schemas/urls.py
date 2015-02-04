from django.conf.urls import patterns, url

urlpatterns = patterns('kraken.apps.schemas.views',
                       url(r'^schemas/$', 'schemas', name='schemas'),
                       url(r'^schemas/versions/$', 'schema_versions', name='schema_versions'),
                       url(r'^schemas/batch_files/$', 'batch_files', name='batch_files'),

                       url(r'^clients/(?P<client_id>\d+)/schemas/create/$', 'create_schema', name='create_schema'),
                       url(r'^schemas/versions/create/$', 'create_version', name='create_version'),
                       url(r'^schemas/files/create/$', 'create_file', name='create_file'),
                       url(r'^schemas/save/$', 'save_schema', name='save_schema'),

                       )
