from django.forms import ModelForm, Form
from ganttly.models import Project, Task, Comment
from django.forms.fields import DateField, CharField, FileField
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

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class FileForm(Form):
    file  = FileField()
    description = CharField(max_length=140)
