# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from cms import views

urlpatterns = patterns('',
	url(r'^$', views.myheartrate_main, name='myheartrate_main'),
	url(r'^upload/$', views.upload_file, name='upload_file'),
	url(r'^login/$', views.myheartrate_login, name='myheartrate_login'),
	url(r'^logout/$', views.myheartrate_logout, name="myheartrate_logout"),

	url(r'^data/(?P<heartratedata_id>\d+)/fundamental/$', views.myheartrate_data_main, name='myheartrate_data_main'),
	url(r'^data/(?P<heartratedata_id>\d+)/bpmgraph/$', views.myheartrate_data_bpmgraph, name='myheartrate_data_bpmgraph'),
	url(r'^data/(?P<heartratedata_id>\d+)/raw/$', views.myheartrate_data_raw, name='myheartrate_data_raw'),
	url(r'^data/(?P<heartratedata_id>\d+)/fft/$', views.myheartrate_data_fft, name='myheartrate_data_fft'),
)
