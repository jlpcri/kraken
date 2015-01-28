from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^kraken/', include('kraken.apps.core.urls', namespace="core")),
    url(r'^kraken/', include('kraken.apps.help.urls', namespace="help")),
    url(r'^kraken/', include('kraken.apps.schemas.urls', namespace="schemas")),
    url(r'^kraken/', include('kraken.apps.users.urls', namespace="users")),
    url(r'^admin/', include(admin.site.urls)),
)
