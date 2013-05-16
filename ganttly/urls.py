from django.conf.urls import patterns, url
from ganttly import views
from django.contrib import admin

urlpatterns = patterns('',
	#url(r'^$', views.index, name='index'),
    url(r'^$','django.contrib.auth.views.login',
        {'template_name':'login.html'}),
	url(r'^projects/$', views.project_list, name='project_list'),
    url(r'^projects/(?P<project_id>\d+)/$', views.project, name='project'),
    #url(r'^projects/(?P<project_id>\d+)/tasks/$', views.task_list, name='task_list'),
    url(r'^projects/(?P<project_id>\d+)/(?P<task_id>\d+)/$', views.task, name='task'),
)