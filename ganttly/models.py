from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	name = models.CharField('Project Name', max_length=50)
	description = models.CharField('Description', max_length=200)
	date = models.DateField('Date Published', auto_now=True)
	admin = models.ForeignKey(User,related_name="owner")
	team = models.ManyToManyField(User,related_name="team")

	def __unicode__(self):
		return self.name

class Task(models.Model):
	name = models.CharField('Name',max_length=50)
	description = models.CharField('Description',max_length=200)
	assigned_to = models.ManyToManyField(User)
	project = models.ForeignKey(Project)
	start = models.DateField('start date')
	finish = models.DateField('finish date')
	has_started = models.BooleanField()
	is_completed = models.BooleanField()

	def __unicode__(self):
		return self.name

class Comment(models.Model):
	comment = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	posted = models.DateTimeField(auto_now_add=True,blank=True)
	parent = models.ForeignKey('self',related_name='comment parent',null=True,blank=True,default=None)
	task = models.ForeignKey(Task)

	def __unicode__(self):
		return self.comment

class File(models.Model):
	name = models.CharField(max_length=50)
	location = models.CharField(max_length=200)
	task = models.ForeignKey(Task)
	added = models.DateTimeField('added date')

	def __unicode__(self):
		return self.name