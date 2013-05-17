from django.conf.urls import patterns, url
from ganttly import views
from django.contrib import admin

urlpatterns = patterns('',
	#url(r'^$', views.index, name='index'),
    url(r'^$','django.contrib.auth.views.login',
        {'template_name':'login.html'}),
    url(r'^logout/$', views.logout, name='logout'),
	url(r'^projects/$', views.project_list, name='project_list'),
    url(r'^projects/add/$', views.project_add, name='project_list'),
    url(r'^projects/(?P<project_id>\d+)/$', views.project, name='project'),
    url(r'^projects/(?P<project_id>\d+)/(?P<task_id>\d+)/$', views.task, name='task'),
    url(r'^projects/(?P<project_id>\d+)/(?P<task_id>\d+)/start/$', views.task_start, name='start_task'),
    url(r'^projects/(?P<project_id>\d+)/add/$', views.task_add, name='task'),
)