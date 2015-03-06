# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from cms.models import HeartRateData

def myheartrate_main(request):
#	return HttpResponse(u'MyHeartRateMain')
	datalist = HeartRateData.objects.all().order_by('id')
	return render_to_response('cms/myheartrate_main.html',
		{'datalist': datalist},
		context_instance=RequestContext(request))