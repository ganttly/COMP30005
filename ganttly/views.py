from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from ganttly.models import Project, Task
from ganttly.forms import ProjectForm, TaskForm
from util.decorators import secure_required, login_required
from datetime import date
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm


def index(request):
    context = {'content': ''}
    return render(request, 'ganttly/index.html', context)

@login_required
def project(request, project_id):
    project = Project.objects.get(id=project_id)
    task_list = Task.objects.filter(project=project_id).order_by('start')

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

@login_required
def project_list(request):
    project_list = Project.objects.filter(admin=request.user)

    context = Context({
        'project_list': project_list,
    })

    return render(request, 'ganttly/projects.html', context)

@login_required
def project_add(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            
            f = ProjectForm(request.POST)
            project = f.save(commit=False)
            project.admin = request.user
            project.save()

            return HttpResponseRedirect('..')

    action = 'add'
    button = 'Add Project'

    context = Context({
        'form': form,
        'action': action,
        'button': button,
    })

    return render(request, 'ganttly/form.html', context)

@login_required
def project_edit(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST or None, instance=project)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('..')

    form = ProjectForm(instance=Project.objects.get(pk=project_id))

    action = 'edit'
    button = 'Edit Project'

    context = Context({
        'form': form,
        'action': action,
        'button': button,
    })

    return render(request, 'ganttly/form.html', context)

@login_required
def task(request, project_id, task_id):
    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=project_id)

    context = Context({
        'project': project,
        'task': task,
    })

    return render(request, 'ganttly/task.html', context)

@login_required
def task_list(request, project_id):
    task_list = Task.objects.all

    context = Context({
        'task_list': task_list,
    })

    return render(request, 'ganttly/tasks.html', context)

@login_required
def task_add(request, project_id):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = Project.objects.get(pk=project_id)
            task.save()
            form.save_m2m()

            return HttpResponseRedirect('..')

    action = 'add'
    button = 'Add Task'

    context = Context({
        'form': form,
        'action': action,
        'button': button,
    })

    return render(request, 'ganttly/form.html', context)

@login_required
def task_edit(request, project_id, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('..')

    form = TaskForm(instance=Task.objects.get(pk=task_id))

    action = 'edit'
    button = 'Edit Task'

    context = Context({
        'form': form,
        'action': action,
        'button': button,
    })

    return render(request, 'ganttly/form.html', context)

@login_required
def task_start(request, project_id, task_id):
    task = Task.objects.get(pk=task_id)
    task.has_started = True
    task.save()

    return HttpResponseRedirect('..')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/ganttly')
    
def register(request):
    if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("..")
	else:
		form = UserCreationForm()
    		return render(request, "register.html", {
		'form': form,
     })
