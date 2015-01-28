from django.conf.urls import patterns, url


urlpatterns = patterns('kraken.apps.users.views',
    url(r'^user_management/$', 'user_management', name='user_management'),
    url(r'^user_update/(?P<user_id>\d+)/$', 'user_update', name='user_update'),
    url(r'^user_delete/(?P<user_id>\d+)/$', 'user_delete', name='user_delete'),
)