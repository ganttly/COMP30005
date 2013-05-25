from django.test import TestCase
from ganttly.models import Project, Task, TaskComment, ProjectComment, File
from django.contrib.auth.models import User
from datetime import datetime


class ProjectTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('joe','joe@news.com','password')
		self.project = Project.objects.create(name="Test",description="Yes testing",admin =self.user,	date=datetime.date)

	def test_eventName(self):
		"""Tests if Event is created with correct name"""
		self.assertEqual(self.project.name, "Test")

	def test_eventAdmin(self):
		"""Tests if Event is created with correct admin"""
		self.assertEqual(self.project.admin, self.user)


class TaskTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('joe','joe@news.com','password')
		self.project = Project.objects.create(name="Test",description="Yes testing",admin =self.user,	date=datetime.date)
		self.event = Task.objects.create(project=self.project, name="Test", description="Yes testing",	start="2013-05-28", finish="2013-06-28", is_completed =False, has_started =True)

	def test_taskName(self):
		"""Tests if Task is created with correct name"""
		self.assertEqual(self.event.name, "Test")

	def test_hasStarted(self):
		"""Tests if Task is has correct has_started status"""
		self.assertTrue(self.event.has_started)	


class TaskCommentTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('joe','joe@news.com','password')
		self.project = Project.objects.create(name="Test",description="Yes testing",admin =self.user,	date=datetime.date)
		self.task = Task.objects.create(project=self.project, name="Test", description="Yes testing",	start="2013-05-28", finish="2013-06-28", is_completed =False, has_started =True)
		self.Taskcomm = TaskComment.objects.create(task=self.task, user = self.user, depth = 1, comment='testcomment', posted=datetime.today)

	def test_commentName(self):
		"""Tests if comment is created with correct comment"""
		self.assertEqual(self.Taskcomm.comment,'testcomment')

	def test_commentdepth(self):
		"""Tests if comment is created with correct depth"""
		self.assertEqual(self.Taskcomm.depth,1)

class ProjectCommentTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('joe','joe@news.com','password')
		self.project = Project.objects.create(name="Test",description="Yes testing",admin =self.user,	date=datetime.date)
		self.Projcomm = ProjectComment.objects.create(project=self.project, user = self.user, depth = 2, comment='testcomment2', posted=datetime.today)

	def test_commentName(self):
		"""Tests if comment is created with correct comment"""
		self.assertEqual(self.Projcomm.comment,'testcomment2')

	def test_commentdepth(self):
		"""Tests if comment is created with correct depth"""
		self.assertEqual(self.Projcomm.depth,2)	

class FileTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('joe','joe@news.com','password')
		self.project = Project.objects.create(name="Test",description="Yes testing",admin =self.user,	date=datetime.date)
		self.task = Task.objects.create(project=self.project, name="Test", description="Yes testing",	start="2013-05-28", finish="2013-06-28", is_completed =False, has_started =True)
		self.file = File.objects.create(task=self.task, name = 'file', added="2013-05-13 12:45")

	def test_commentName(self):
		"""Tests if file is created with correct name"""
		self.assertEqual(self.file.name,'file')
