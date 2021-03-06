from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	admin = models.ForeignKey(User,related_name="owner")
	name = models.CharField('Project Name', max_length=50)
	description = models.CharField('Description', max_length=200)
	date = models.DateField('Date Published', auto_now=True)
	team = models.ManyToManyField(User,related_name="team")

	def __unicode__(self):
		return self.name

class Task(models.Model):
	project = models.ForeignKey(Project)
	name = models.CharField('Name',max_length=50)
	description = models.CharField('Description',max_length=200)
	assigned_to = models.ManyToManyField(User)
	start = models.DateField('start date')
	finish = models.DateField('finish date')
	has_started = models.BooleanField()
	is_completed = models.BooleanField()

	def __unicode__(self):
		return self.name

class TaskComment(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    path = models.CommaSeparatedIntegerField(max_length=50, blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)
    comment = models.CharField(max_length=400)
    posted = models.DateTimeField(auto_now_add=True)
	
    def __unicode__(self):
        return self.comment
	    
class ProjectComment(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    path = models.CommaSeparatedIntegerField(max_length=50, blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)
    comment = models.CharField(max_length=400)
    posted = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.comment

class File(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    description = models.CharField(max_length=50)
    filename = models.CharField(max_length=100)
    extension = models.CharField(max_length=20)
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name