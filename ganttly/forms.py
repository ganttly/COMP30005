from django.forms import ModelForm
from ganttly.models import Project, Task
from django.forms.fields import DateField
from django.forms.extras.widgets import SelectDateWidget

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name','description']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name','description','assigned_to','start','finish']
    start = DateField(widget=SelectDateWidget)
    finish = DateField(widget=SelectDateWidget)