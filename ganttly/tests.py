from django.test import TestCase
from ganttly.models import Project
from django.contrib.auth.models import User
from datetime import datetime


class ProjectTest(TestCase):
    def setUp(self):
		self.user = User.objects.create_user('joe','joe@news.com', 'password')
		self.event = Project.objects.create(name="Test",description="Yes testing",admin =self.user,	date=datetime.date)
	def test_eventName(self):
		"""Tests if Event is created with correct name"""
		self.assertEqual(self.event.name, "Test")

	def test_eventAdmin(self):
		"""Tests if Event is created with correct admin"""
		self.assertEqual(self.event.admin, self.user)

	def test_eventDate(self):
		"""Tests if Event is not equal to user"""
		self.assertNotEqual(self.event.date, self.user)
