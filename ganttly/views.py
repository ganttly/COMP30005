import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template import Context, loader
from ganttly.models import Project, Task, ProjectComment, TaskComment, File
from ganttly.forms import ProjectForm, TaskForm, UserCreateForm, ProjectCommentForm, TaskCommentForm, FileForm
from util.decorators import secure_required, login_required, project_admin_required
from datetime import date
from django.contrib import auth
from ganttly.util.upload import UploadFile

def index(request):
    context = {'content': ''}
    return render(request, 'ganttly/index.html', context)

@login_required     
def project(request, project_id):

     #Get form case a new comment was posted
    form = ProjectCommentForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.project = get_object_or_404(Project, id=project_id)
            new_comment.user = request.user
            parent_id = form['parent'].value()
            
            if parent_id == '':
                #Set a blank path then save it to get an ID
                new_comment.path = ''
                new_comment.save()
                new_comment.path = str(new_comment.id)
            else:
                #Get the parent node
                parent = get_object_or_404(ProjectComment, id=parent_id)
                new_comment.depth = parent.depth + 1
                new_comment.path = str(parent.path)
                
                #Store parents path then apply comment ID
                new_comment.save()
                new_comment.path += ',' + str(new_comment.id)
                
            #Final save for parents and children
            new_comment.save()
            return HttpResponseRedirect('.')

    # Get the project and tasks objects
    project = Project.objects.get(id=project_id)
    task_list = Task.objects.filter(project=project_id).order_by('start')

    #Retrieve all comments for the project
    comments = ProjectComment.objects.filter(project=project_id)
    
    #Transform the comment's list of string paths to a list of integers
    for i in range(len(comments)):
        comments[i].path = ([int(num) for num in comments[i].path.split(',')])
    
    #Order the list of comments by their paths
    comments = sorted(comments, key=lambda x: x.path)

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
        'form': form,
        'comments': comments,
        'first_date': first_date,
        'last_date': last_date,
        'total_days': total_days,
    })

    return render(request, 'ganttly/project.html', context)

@login_required
def project_list(request):
    project_list = Project.objects.filter(admin=request.user)
    #project_list = Project.objects.filter(team=request.user)

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
    #Get project object
    project = get_object_or_404(Project, id=project_id)

    #Delete all tasks within the project
    tasks = Task.objects.filter(project=project)
    for t in tasks:
        delete_task(t.id)
    
    #Delete comments and the project itself
    ProjectComment.objects.filter(project=project).delete();
    project.delete()
    
    return HttpResponseRedirect('../..')

@login_required
def task(request, project_id, task_id):

    #Get task and project objects
    task = get_object_or_404(Task, id = task_id)
    project = get_object_or_404(Project, id = project_id)
    
    #Get form case a new comment was posted
    commentForm = TaskCommentForm(prefix='comment')
    file_form = FileForm(prefix='upload');

    if request.method == "POST":
        file_form = FileForm(request.POST, request.FILES, prefix='upload')
        commentForm = TaskCommentForm(request.POST or None, prefix='comment')

        if commentForm.is_valid():
            new_comment = commentForm.save(commit=False)
            new_comment.task = get_object_or_404(Task, id=task_id)
            new_comment.user = request.user
            parent_id = commentForm['parent'].value()
            
            if parent_id == '':
                #Set a blank path then save it to get an ID
                new_comment.path = ''
                new_comment.save()
                new_comment.path = str(new_comment.id)
            else:
                #Get the parent node
                parent = get_object_or_404(TaskComment, id=parent_id)
                new_comment.depth = parent.depth + 1
                new_comment.path = str(parent.path)
                
                #Store parents path then apply comment ID
                new_comment.save()
                new_comment.path += ',' + str(new_comment.id)
                
            #Final save for parents and children
            new_comment.save()
            return HttpResponseRedirect('.')

        if file_form.is_valid():
            data = file_form.cleaned_data

            task_file = File()

            task_file.task = task
            task_file.description = data['description']
            task_file.user = request.user
            task_file.filename = os.path.basename(request.FILES['upload-file'].name)
            task_file.extension = os.path.splitext(request.FILES['upload-file'].name)[1]

            task_file.save()

            UploadFile(request.FILES['upload-file'], task_file.id)
            return HttpResponseRedirect('.')

    #Retrieve all comments for the task
    comments = TaskComment.objects.filter(task=task_id)
    
    #Transform the comment's list of string paths to a list of integers
    for i in range(len(comments)):
        comments[i].path = ([int(num) for num in comments[i].path.split(',')])
    
    #Order the list of comments by their paths
    comments = sorted(comments, key=lambda x: x.path)

    files = File.objects.filter(task=task_id)
    
    context = Context({
        'forms':[commentForm, file_form],
        'project': project,
        'task': task,
        'action': '',
        'button': 'Upload',
        'comments':comments,
        'files': files
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
    
    #Call function that delete all task related entries
    delete_task(task_id)
    
    return HttpResponseRedirect('../..')
    
def delete_task(task_id):
    task = get_object_or_404(Task, id=task_id)
    
    #Delete comments on task
    TaskComment.objects.filter(task=task).delete();
    
    #Delete task itself
    task.delete()
    
    #Delete uploaded documents

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
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("..")
    else:
        form = UserCreateForm()
        return render(request, "register.html", {
        'form': form,
        })

@login_required
def download_file(request, project_id, task_id, file_id):
    down_file = get_object_or_404(File, id=file_id)

    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + down_file.filename
    response['X-Sendfile'] = 'C:/Users/Brendan/BitNami DjangoStack projects/COMP30005/ganttly/uploads/' + str(down_file.id) + down_file.extension

    return response