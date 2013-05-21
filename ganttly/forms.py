
from django.forms import ModelForm, HiddenInput, Textarea
from django.forms.fields import DateField, EmailField, CharField
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ganttly.models import Project, Task, ProjectComment, TaskComment

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name','description']

class TaskForm(ModelForm):
    start = DateField(widget=SelectDateWidget)
    finish = DateField(widget=SelectDateWidget)

    class Meta:
        model = Task
        fields = ['name','description','assigned_to','start','finish']

class TaskCommentForm(ModelForm):
    # Hidden value for the parent
    parent = CharField(widget=HiddenInput(attrs={'class':'parent'}), required=False)
    comment = CharField(widget=Textarea(attrs={'cols': 10, 'rows': 5}), label="Your comment:")
    
    class Meta:
        model = TaskComment
        fields = ['comment']