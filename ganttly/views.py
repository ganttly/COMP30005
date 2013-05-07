from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader
from ganttly.models import Project

def index(request):
    context = {'content': 'hello WORLD'}
    return render(request, 'ganttly/index.html', context)

def project_list(request):
    project_list = Project.objects.all

    context = Context({
        'project_list': project_list,
    })

    return render(request, 'ganttly/projects.html', context)