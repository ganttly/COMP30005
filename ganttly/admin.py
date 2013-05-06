from django.contrib import admin
from ganttly.models import Project
from ganttly.models import Task
from ganttly.models import Comment

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)