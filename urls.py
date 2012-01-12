from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler404 = 'horasdsconapp.views.handle_error404'
handler500 = 'horasdsconapp.views.handle_error500'

urlpatterns = patterns('horasdsconapp.views',
    (r'^$', 'index'),
    (r'^token=(?P<token>\d+)/$', 'index_authenticated')
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
