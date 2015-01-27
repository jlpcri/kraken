from django.conf.urls import patterns, url

urlpatterns = patterns('kraken.apps.schemas.views',
                       url(r'^$', 'schemas', name='schemas'),
                       url(r'/versions/$', 'schema_versions', name='schema_versions'),
                       url(r'/batch_files/$', 'batch_files', name='batch_files')

                       )
