import os
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from horasdsconapp.views import home, done, logout, error
admin.autodiscover()

handler404 = 'horasdsconapp.views.handle_error404'
handler500 = 'horasdsconapp.views.handle_error500'

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'', include('social_auth.urls')),
)

#urlpatterns = patterns('',
#    # Examples:
#    # url(r'^$', 'horasdscon.views.home', name='home'),
#    # url(r'^horasdscon/', include('horasdscon.foo.urls')),
#
#    # Uncomment the admin/doc line below to enable admin documentation:
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
#
#    # Uncomment the next line to enable the admin:
#    url(r'^admin/', include(admin.site.urls)),
#
#)
