# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from cms import views

urlpatterns = patterns('',
	url(r'^$', views.myheartrate_main, name='myheartrate_main'),
	url(r'^upload/$', views.upload_file, name='upload_file'),

	url(r'^data/(?P<heartratedata_id>\d+)/fundamental/$', views.myheartrate_data_main, name='myheartrate_data_main'),
	url(r'^data/(?P<heartratedata_id>\d+)/bpmgraph/$', views.myheartrate_data_bpmgraph, name='myheartrate_data_bpmgraph'),
	url(r'^data/(?P<heartratedata_id>\d+)/raw/$', views.myheartrate_data_raw, name='myheartrate_data_raw')
)
