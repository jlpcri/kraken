from django.conf.urls import patterns, url

urlpatterns = patterns('kraken.apps.help.views',
                       url(r'^guide/$', 'help_guide', name='help_guide'),
                       url(r'^faq/$', 'help_faq', name='help_faq'),
                       )