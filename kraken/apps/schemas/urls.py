from django.conf.urls import patterns, url

urlpatterns = patterns('kraken.apps.schemas.views',
                       url(r'^schemas/$', 'schemas', name='schemas'),
                       url(r'^schemas/versions/$', 'schema_versions', name='schema_versions'),
                       url(r'^schemas/batch_files/$', 'batch_files', name='batch_files')

                       )
