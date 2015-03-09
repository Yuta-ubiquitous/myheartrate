# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from cms.models import HeartRateData, Content
from datetime import datetime
import sys, re

def myheartrate_main(request):
	return render_to_main(request)

def myheartrate_data_main(request, heartratedata_id):
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	return render_to_response('basecontent.html',
		context_instance=RequestContext(request))

#def myheartrate_data_main(request, heartratedata_id):
#	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
#	datalist = heartratedata.contents.all().order_by('id')
#	text = ''
#	for data in datalist:
#		text += ' ' + str(data.bpm)
#	return HttpResponse(text)

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
			return render_to_main(request)
		else:
			return render_to_main(request)
			# handle_uploaded_file(request.FILES['file'])
			# return HttpResponseRedirect('/myheartrate')
	return render_to_main(request)

def render_to_main(request):
	datalist = HeartRateData.objects.all().order_by('id')
	return render_to_response('cms/myheartrate_main.html',
			{'datalist': datalist},
			context_instance=RequestContext(request))

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
