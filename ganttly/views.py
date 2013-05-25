from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from ganttly.models import Project, Task, Comment
from ganttly.forms import ProjectForm, TaskForm, CommentForm, FileForm
from util.decorators import secure_required, login_required, project_admin_required
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
    #project_list = Project.objects.filter(admin=request.user)
    project_list = Project.objects.filter(team=request.user)

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
            project = form.save(commit=False)
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
@project_admin_required
def project_edit(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST or None, instance=project)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()

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
@project_admin_required
def project_delete(request, project_id):
    return HttpResponseRedirect('../..')

@login_required
def task(request, project_id, task_id):
    comment_form = CommentForm()
    file_form = FileForm()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.task = Task.objects.get(id=task_id)
            comment.posted
            comment.save()

            comment_form = CommentForm()

        file_form = FileForm(request.POST)
        if file_form.is_valid():
            file = file_form.save(commit=False)
            file.user = request.user
            file.task = Task.objects.get(id=task_id)
            file.posted
            file.save()

            file_form = FileForm()

    action = task_id

    task = Task.objects.get(id=task_id)
    project = Project.objects.get(id=project_id)
    comments = Comment.objects.filter(task_id=task_id)

    forms = [comment_form, file_form]
    buttons = ['Add Comment', 'Add File']

    context = Context({
        'project': project,
        'task': task,
        'comments': comments,
        'forms': forms,
        'action': action,
        'buttons': buttons,
    })

    return render(request, 'ganttly/task.html', context)

@login_required
@project_admin_required
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
@project_admin_required
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
    if task.has_started:
        task.has_started = False
    else:
        task.has_started = True
    task.save()

    return HttpResponseRedirect('..')

@login_required
@project_admin_required
def task_delete(request, project_id, task_id):
    return HttpResponseRedirect('../..')

@login_required
def task_finish(request, project_id, task_id):
    task = Task.objects.get(pk=task_id)
    if task.has_started:
        task.is_completed = True
    
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
            return HttpResponseRedirect("../projects")
    else:
        form = UserCreationForm()

    action = 'register'
    button = 'Register'

    context = Context({
        'form': form,
        'action': action,
        'button': button,
    })

    return render(request, 'ganttly/form.html', context)
