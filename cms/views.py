# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from cms.models import HeartRateData, Content
from datetime import datetime, timedelta
import sys, re, pytz

def myheartrate_main(request):
	return render_to_main(request)

def myheartrate_data_main(request, heartratedata_id):
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	return render_to_response('cms/myheartrate_fundamental.html',
		{'heartratedata_id' : heartratedata_id},
		context_instance=RequestContext(request))

def myheartrate_data_bpmgraph(request, heartratedata_id):
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	chartData = ''
	JST = pytz.timezone('Asia/Tokyo')
	for data in datalist:
		chartData += '{"time":"'+data.time.astimezone(JST).strftime("%H:%M:%S") +'","value":' +str(data.bpm) +'},'

	firstData = datalist[0].time.astimezone(JST).strftime("(%Y,%m,%d,%H,%M,%S)")
	lastData = datalist[len(datalist)-1].time.astimezone(JST).strftime("(%Y,%m,%d,%H,%M,%S)")

	return render_to_response('cms/myheartrate_bpmgraph.html',
		dict(heartratedata_id=heartratedata_id,
			chartData=chartData,
			firstData=firstData,
			lastData=lastData),
		context_instance=RequestContext(request))

def myheartrate_data_raw(request, heartratedata_id):
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	return render_to_response('cms/myheartrate_bpmraw.html',
		dict(heartratedata_id=heartratedata_id,
			datalist=datalist),
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
			text_file_to_db(text, get_first_time(text))
			return render_to_main(request)
		else:
			return render_to_main(request)
			# handle_uploaded_file(request.FILES['file'])
			# return HttpResponseRedirect('/myheartrate')
	return render_to_main(request)

def render_to_main(request):
	datalist = HeartRateData.objects.all().order_by('id')
	return render_to_response('cms/myheartrate_main.html',
			{'datalist': datalist[::-1]},
			context_instance=RequestContext(request))

def text_file_to_db(text, firstTime):
	heartRateData = HeartRateData()
	heartRateData.user = 'yuta.takahashi'
	heartRateData.save()
	array = text.split(' ')
	i = 0
	second = timedelta(0)
	for element in array:
		if i > 5:
			m = re.match(r'\d+', element)
			if m != None:
				content = Content()
				content.heartratedata = heartRateData
				content.time = firstTime + second
				content.bpm = int(element)
				print(content)
				content.save()
				second += timedelta(seconds=1)
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
				hour, minute = m.groups()
		elif i == 5:
			m = re.match(r'duration_(\d+)min-(\d+)sec', element)
			if m == None:
				return False
			else:
				dmin, dsec = m.groups()
		else:
			m = re.match(r'\d*', element)
			if m == None:
				return False
		i += 1
	return True

def get_first_time(text):
	array = text.split(' ')
	lastTime = datetime.now()
	lastTime = lastTime.replace(second=0, microsecond=0)
	duration = timedelta(0)
	i = 0
	for element in array:
		if i == 3:
			m = re.match(r'date_(\d+)-(\d+)', element)
			month, day = m.groups()
			lastTime = lastTime.replace(month=int(month), day=int(day))
		elif i == 4:
			m = re.match(r'at_(\d+):(\d+)', element)
			hour, minute = m.groups()
			lastTime = lastTime.replace(hour=int(hour), minute=int(minute))
		elif i == 5:
			m = re.match(r'duration_(\d+)min-(\d+)sec', element)
			dmin, dsec = m.groups()
			duration = timedelta(seconds=int(dmin)*60+int(dsec))
			break
		i += 1
	return lastTime - duration
