from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'COMP30005.views.home', name='home'),
    # url(r'^COMP30005/', include('COMP30005.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^polliebyte/', include('polliebyte.urls')),
    url(r'^ganttly/', include('ganttly.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
