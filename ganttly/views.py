from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from ganttly.models import Project, Task

def index(request):
    context = {'content': ''}
    return render(request, 'ganttly/index.html', context)

def project_list(request):
    project_list = Project.objects.all

    context = Context({
        'project_list': project_list,
    })

    return render(request, 'ganttly/projects.html', context)

def task_list(request, project_id):
    task_list = Task.objects.all

    context = Context({
        'task_list': task_list,
    })

    return render(request, 'ganttly/tasks.html', context)

def project(request, project_id):
    project = Project.objects.get(id=project_id)

    context = Context({
    	'project': project,
    })

    return render(request, 'ganttly/project.html', context)

def task(request, project_id, task_id):
    context = Context({
        'project': 'put project here',
        'task': 'put task here',
    })

    return render(request, 'ganttly/task.html', context)