from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from ganttly.models import Project, Task
from datetime import date

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
    task_list = Task.objects.filter(project=project_id)

    total_days = 0
    first_date = 0
    last_date = 0

    if len(task_list) > 0:
        first_date = task_list.order_by('start')[0].start
        last_date = task_list.order_by('-finish')[0].finish
        total_days = (last_date - first_date).days + 1

    context = Context({
    	'project': project,
        'task_list': task_list,
        'first_date': first_date,
        'last_date': last_date,
        'total_days': total_days,
    })

    return render(request, 'ganttly/project.html', context)

def task(request, project_id, task_id):
    context = Context({
        'project': 'put project here',
        'task': 'put task here',
    })

    return render(request, 'ganttly/task.html', context)