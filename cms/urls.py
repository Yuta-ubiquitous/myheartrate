# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from cms import views

urlpatterns = patterns('',
	url('', views.myheartrate_main, name='myheartrate_main'),
)