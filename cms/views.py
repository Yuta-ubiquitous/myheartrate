# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from cms.models import HeartRateData, Content
from cms.forms import Login_form
from datetime import datetime, timedelta
from numpy import *
from numpy.fft import fft, fftfreq
import sys, re, pytz

#def myheartrate_data_main(request, heartratedata_id):
#	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
#	datalist = heartratedata.contents.all().order_by('id')
#	text = ''
#	for data in datalist:
#		text += ' ' + str(data.bpm)
#	return HttpResponse(text)

def myheartrate_login(request):
	if request.POST:
		form = Login_form(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('cms:myheartrate_main')
	else:
		form = Login_form()
	return render(request, 'cms/myheartrate_login.html', {'form' : form})

def myheartrate_logout(request):
	logout(request)
	return redirect('cms:myheartrate_main')

def text_file_to_db(text, infolist, username):
	heartRateData = HeartRateData()
	heartRateData.user = username
	heartRateData.firstTime = infolist['firstTime']
	heartRateData.endTime = infolist['endTime']
	heartRateData.points = infolist['points']
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
				content.time = infolist['firstTime'] + second
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
				print('invalied : Profile')
				return False
		elif i == 1:
			s = re.search(r'Values$', element)
			if s == None:
				print('invalied : Values')
				return False
		elif i == 2:
			m = re.match(r'stored', element)
			if m == None:
				print('invalied : stored')
				return False
		elif i == 3:
			m = re.match(r'date_(\d+)-(\d+)', element)
			if m == None:
				print('invalied : data_**-**')
				return False
			else:
				month, day = m.groups()
		elif i == 4:
			m = re.match(r'at_(\d+):(\d+)', element)
			if m == None:
				print('invalied : at_**:**')
				return False
			else:
				hour, minute = m.groups()
		elif i == 5:
			m = re.match(r'duration(_+)(\d+)min(-+)(\d+)sec', element)
			if m == None:
				print('invalied : duration_**min-**sec')
				return False
			else:
				print(m.groups())
				buf0, dmin, buf1, dsec = m.groups()
		else:
			m = re.match(r'\d*', element)
			if m == None:
				return False
		i += 1
	return True

def get_data_info(text):
	array = text.split(' ')
	endTime = datetime.now().replace(second=0, microsecond=0)
	duration = timedelta(0)
	i = 0
	count = 0
	for element in array:
		if i == 3:
			m = re.match(r'date_(\d+)-(\d+)', element)
			month, day = m.groups()
			endTime = endTime.replace(month=int(month), day=int(day))
		elif i == 4:
			m = re.match(r'at_(\d+):(\d+)', element)
			hour, minute = m.groups()
			endTime = endTime.replace(hour=int(hour), minute=int(minute))
		elif i == 5:
			m = re.match(r'duration(_+)(\d+)min(-+)(\d+)sec', element)
			buf0,dmin, buf1, dsec = m.groups()
			duration = timedelta(seconds=int(dmin) * 60 + int(dsec))
		else:
			m = re.match(r'\d+', element)
			if m != None:
				count += 1
		i += 1
	infolist = {
		'firstTime': endTime - duration,
		'endTime': endTime,
		'points' : count
	}
	return infolist

def upload_file(request):
	# print('upload_file')
	if request.method == 'POST':
		# print(request.POST)
		# print(request.FILES)
		file = request.FILES['uploadfile']
		username = request.POST.get('username', default='error')
		text = ''
		for chunk in file.chunks():
			text += chunk.decode(sys.stdin.encoding)

		if validate_text_file(text):
			infolist = get_data_info(text)
			text_file_to_db(text, infolist, username)
			return redirect('cms:myheartrate_main', notice='success')
		else:
			return redirect('cms:myheartrate_main', notice='failed')
			# handle_uploaded_file(request.FILES['file'])
			# return HttpResponseRedirect('/myheartrate')
	return redirect('cms:myheartrate_main')

def myheartrate_main(request):
	datalist = HeartRateData.objects.all().order_by('id')
	if request.GET.__contains__("notice"):
		notice = request.GET["notice"]
		if notice == 'success':
			print('success : Your data is valied.')
			return render_to_response('cms/myheartrate_main.html',
				dict(datalist=datalist[::-1], is_success=True),
				context_instance=RequestContext(request))
		elif notice == 'failed':
			print('failed : Your data is invalied.')
			return render_to_response('cms/myheartrate_main.html',
				dict(datalist=datalist[::-1], is_failed=True),
				context_instance=RequestContext(request))
	return render_to_response('cms/myheartrate_main.html',
		{'datalist': datalist[::-1]},
		context_instance=RequestContext(request))

def myheartrate_data_main(request, heartratedata_id):
	if not request.user.is_authenticated():
		return redirect('cms:myheartrate_main')
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	minute = int(heartratedata.points / 60)
	second = heartratedata.points % 60
	return render_to_response('cms/myheartrate_fundamental.html',
		dict(heartratedata_id=heartratedata_id,
			heartratedata=heartratedata,
			minute=minute,
			second=second),
		context_instance=RequestContext(request))

def myheartrate_data_bpmdata(request, heartratedata_id):
	if not request.user.is_authenticated():
		return redirect('cms:myheartrate_main')
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	return render_to_response('cms/myheartrate_bpmdata.html',
		dict(heartratedata_id=heartratedata_id,
			datalist=datalist),
		context_instance=RequestContext(request))

def myheartrate_data_bpmgraph(request, heartratedata_id):
	if not request.user.is_authenticated():
		return redirect('cms:myheartrate_main')
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	chartData = ''
	JST = pytz.timezone('Asia/Tokyo')
	for data in datalist:
		chartData += '{"time":"'+data.time.astimezone(JST).strftime("%H:%M:%S") +'","value":' +str(data.bpm) +'},'
	return render_to_response('cms/myheartrate_bpmgraph.html',
		dict(heartratedata_id=heartratedata_id,
			chartData=chartData),
		context_instance=RequestContext(request))

def fft_calc(heartratedata_id):
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	bpmlist = []
	for data in datalist:
		bpmlist.append(data.bpm)
	inputSignal = array(bpmlist)
	fourier = fft(inputSignal)
	# <class 'numpy.ndarray'> complex128
	fourier_result = []
	frequency = fftfreq(len(fourier))
	i = 0
	for z in fourier[:len(fourier)/2+1]:
		values = {}
		values.update( { "id" : i } )
		values.update( { "freq" : frequency[i] } )
		values.update( { "abs" : abs(z) } )
		values.update( { "real" : z.real } )
		values.update( { "imag" : z.imag } )
		i += 1
		fourier_result.append(values)
	return fourier_result

def myheartrate_data_spectrumdata(request, heartratedata_id):
	fourier=fft_calc(heartratedata_id)
	return render_to_response('cms/myheartrate_spectrumdata.html',
		dict(heartratedata_id=heartratedata_id,
			fourier=fourier),
		context_instance=RequestContext(request))

def myheartrate_data_spectrumgraph(request, heartratedata_id):
	fourier = fft_calc(heartratedata_id)
	fourier_data = ''
	for z in fourier[1::]:
		fourier_data+='{"freq":'+str(log10(z['freq']))+',"value":'+str(z['abs']) +'},'
	return render_to_response('cms/myheartrate_spectrumgraph.html',
		dict(heartratedata_id=heartratedata_id, chartData=fourier_data),
		context_instance=RequestContext(request))

def myheartrate_data_poincareplot(request, heartratedata_id):
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	poincare = []
	i = 0
	buf = datalist[0].bpm
	for data in datalist[1::]:
		poincare.append([buf,data.bpm])
		buf = data.bpm
	poincare_data = ''
	for data in poincare:
		poincare_data+='{"xp":'+str(data[0])+',"yp":'+str(data[1]) +'},'
	return render_to_response('cms/myheartrate_poincareplot.html',
		dict(heartratedata_id=heartratedata_id,chartData=poincare_data),
		context_instance=RequestContext(request))

def myheartrate_data_histgram(request, heartratedata_id):
	WIDTH_PLUS = 10
	heartratedata = get_object_or_404(HeartRateData, pk=heartratedata_id)
	datalist = heartratedata.contents.all().order_by('id')
	min = 1000
	max = 0
	for data in datalist:
		min = min if min < data.bpm else data.bpm
		max = max if max > data.bpm else data.bpm
	histgram = {}
	for num in range(min - WIDTH_PLUS, max + 1 + WIDTH_PLUS):
		histgram.update({num : 0})
	for data in datalist:
		histgram[data.bpm] += 1
	histgram_data = ''
	for num in range(min - WIDTH_PLUS, max + 1 + WIDTH_PLUS):
		histgram_data+='{"width":'+str(num)+',"value":'+str(histgram[num])+'},'
	return render_to_response('cms/myheartrate_histgram.html',
		dict(heartratedata_id=heartratedata_id,chartData=histgram_data),
		context_instance=RequestContext(request))
