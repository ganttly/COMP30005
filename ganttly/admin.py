from django.contrib import admin
from ganttly.models import Project, Task, ProjectComment, TaskComment

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(ProjectComment)
admin.site.register(TaskComment)
