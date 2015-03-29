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
	url(r'^data/(?P<heartratedata_id>\d+)/bpmdata/$', views.myheartrate_data_bpmdata, name='myheartrate_data_bpmdata'),
	url(r'^data/(?P<heartratedata_id>\d+)/bpmgraph/$', views.myheartrate_data_bpmgraph, name='myheartrate_data_bpmgraph'),
	url(r'^data/(?P<heartratedata_id>\d+)/spectrumdata/$', views.myheartrate_data_spectrumdata, name='myheartrate_data_spectrumdata'),
	url(r'^data/(?P<heartratedata_id>\d+)/spectrumgraph/$', views.myheartrate_data_spectrumgraph, name='myheartrate_data_spectrumgraph'),
	url(r'^data/(?P<heartratedata_id>\d+)/poincareplot/$', views.myheartrate_data_poincareplot, name='myheartrate_data_poincareplot'),
	url(r'^data/(?P<heartratedata_id>\d+)/histgram/$', views.myheartrate_data_histgram, name='myheartrate_data_histgram'),
)
