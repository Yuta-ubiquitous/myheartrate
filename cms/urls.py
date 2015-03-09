# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from cms import views

urlpatterns = patterns('',
	url(r'^$', views.myheartrate_main, name='myheartrate_main'),
	url(r'^upload/$', views.upload_file, name='upload_file'),
)
