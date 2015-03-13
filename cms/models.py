# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime

class HeartRateData(models.Model):
	pub_date = models.DateTimeField(default=datetime.now)
	user = models.CharField(max_length=50)
	firstTime = models.DateTimeField(default=datetime.now)
	endTime = models.DateTimeField(default=datetime.now)
	points = models.IntegerField(blank=False, default=0)

	def __str__(self):
		return str(self.id)

class Content(models.Model):
	heartratedata = models.ForeignKey(HeartRateData, related_name='contents')
	time = models.DateTimeField('date published')
	bpm = models.IntegerField(blank=False, default=0)

	def __str__(self):
		return str(self.bpm)

class Tag(models.Model):
	heartratedata = models.ForeignKey(HeartRateData, related_name='tags')
	tag = models.CharField(max_length=64)

	def __str__(self):
		return self.tag
