# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from cms.models import HeartRateData, Content
from datetime import datetime
import sys, re

def myheartrate_main(request):
	#	return HttpResponse(u'MyHeartRateMain')
	datalist = HeartRateData.objects.all().order_by('id')
	return render_to_response('cms/myheartrate_main.html',
	{'datalist': datalist},
	context_instance=RequestContext(request))

def upload_file(request):
	print('upload_file')
	if request.method == 'POST':
		print(request.POST)
		print(request.FILES)
		file = request.FILES['uploadfile']
		text = ''
		for chunk in file.chunks():
			text += chunk.decode(sys.stdin.encoding)

		if validate_text_file(text):
			text_file_to_db(text)
			return HttpResponse(u'Success')
		else:
			return HttpResponse(text)
			# handle_uploaded_file(request.FILES['file'])
			# return HttpResponseRedirect('/myheartrate')
	return HttpResponse(u'failed')

def text_file_to_db(text):
	heartRateData = HeartRateData()
	heartRateData.user = 'yuta.takahashi'
	heartRateData.save()
	array = text.split(' ')
	i = 0
	for element in array:
		if i > 5:
			m = re.match(r'\d+', element)
			if m != None:
				content = Content()
				content.heartratedata = heartRateData
				content.time = datetime.now()
				content.bpm = int(element)
				print(content)
				content.save()
		i += 1

def validate_text_file(text):
	array = text.split(' ')
	if len(array) < 7:
		return False
	i = 0
	for element in array:
		if i == 0:
			m = re.match(r'^Profile', element)
			if m == None:
				return False
		elif i == 1:
			s = re.search(r'Values$', element)
			if s == None:
				return False
		elif i == 2:
			m = re.match(r'stored', element)
			if m == None:
				return False
		elif i == 3:
			m = re.match(r'date_(\d+)-(\d+)', element)
			if m == None:
				return False
			else:
				month, day = m.groups()
		elif i == 4:
			m = re.match(r'at_(\d+):(\d+)', element)
			if m == None:
				return False
			else:
				hour, second = m.groups()
		elif i == 5:
			m = re.match(r'duration_(\d+)min-(\d+)sec', element)
			if m == None:
				return False
			else:
				dhour, dsec = m.groups()
		else:
			m = re.match(r'\d*', element)
			if m == None:
				return False
		i += 1
	return True
