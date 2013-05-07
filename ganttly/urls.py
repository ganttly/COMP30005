from django.conf.urls import patterns, url
from ganttly import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^projects/', views.project_list, name='index'),
    url(r'^(?P<project_id>\d+)/$', views.index, name='index'),
    url(r'^(?P<project_id>\d+)/tasks/$', views.index, name='index'),
)