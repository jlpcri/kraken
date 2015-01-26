from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^kraken/$', 'kraken.apps.core.views.landing', name='landing'),
    #url(r'^kraken/', include('kraken.apps.core.urls')),
    url(r'^kraken/', include('kraken.apps.help.urls')),
    url(r'^kraken/', include('kraken.apps.schemas.urls')),
    url(r'^kraken/', include('kraken.apps.users.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
