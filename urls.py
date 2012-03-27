import os
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover
from horasdsconapp.views import home, existeplanilha, logout, error, login_error, custom_error, complete, criarplanilha, projetos, ajax_empresas, ajax_projetos
import settings

dajaxice_autodiscover()

admin.autodiscover()

handler404 = 'horasdsconapp.views.handle_error404'
handler500 = 'horasdsconapp.views.handle_error500'

if settings.util.getEntry('geral', 'ISDEV') == 'TRUE':
    urlpatterns = staticfiles_urlpatterns()

urlpatterns = patterns('',
    url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
    url(r'^$', home, name='home'),
    url(r'^existeplanilha/$', existeplanilha, name='existeplanilha'),
    url(r'^criarplanilha/$', criarplanilha, name='criarplanilha'),
    url(r'^projetos/$', projetos, name='projetos'),
    url(r'^ajax/empresas/$', ajax_empresas, name='ajax_empresas'),
    url(r'^ajax/projetos/$', ajax_projetos, name='ajax_projetos'),
    url(r'^error/$', error, name='error'),
    url(r'^login/error/$', login_error, name='error'),
    url(r'^custom_error/$', custom_error, name='custom_error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^complete/(?P<backend>[^/]+)/$', complete, name='complete'),
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
