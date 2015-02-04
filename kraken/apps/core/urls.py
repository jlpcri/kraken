from django.conf.urls import patterns, url
from django.contrib import admin
from kraken.apps.core import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.landing, name="landing"),
    url(r'^home/$', views.home, name="home"),
    url(r'^signin/$', views.sign_in, name="sign_in"),
    url(r'^signout/$', views.sign_out, name="sign_out"),

    url(r'^clients/$', views.clients_list, name='clients_list'),
    url(r'^clients/client_schemas/$', views.client_schemas_list, name='client_schemas_list'),
    url(r'^clients/create/$', views.create_client, name='create_client'),
)
