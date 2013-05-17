from django.forms import ModelForm
from ganttly.models import Project, Task

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name','description']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name','description','assigned_to','start','finish']