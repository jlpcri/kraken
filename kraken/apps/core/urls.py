from django.conf.urls import patterns, url
from django.contrib import admin
from kraken.apps.core import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.landing, name="landing"),
    url(r'^home/$', views.home, name="home"),
    url(r'^signin/$', views.sign_in, name="sign_in"),
    url(r'^signout/$', views.sign_out, name="sign_out"),

    url(r'^clients/new/$', views.client_new, name='client_new'),
    url(r'^clients/$', views.clients_list, name='clients_list'),


)
