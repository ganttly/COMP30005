from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	date = models.DateTimeField('date published')
	admin = models.ForeignKey(User)

	def __unicode__(self):
		return self.name

class Task(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	start = models.DateTimeField('start date')
	finish = models.DateTimeField('finish date')
	has_started = models.BooleanField()
	is_completed = models.BooleanField()

	def __unicode__(self):
		return self.name

class Comment(models.Model):
	comment = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	posted = models.DateTimeField()

