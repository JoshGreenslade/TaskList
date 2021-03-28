from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Project
from .models import Task
from .forms import ProjectForm
from .forms import TaskForm

# Create your views here.


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'projects/project_list.html', {'projects': projects})


def save_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            projects = Project.objects.all()
            data['html_project_list'] = render_to_string(
                'projects/includes/partial_project_list.html', {'projects': projects})
        else:
            data['form_is_valid'] = False

    context = {'form': form}
    data['html_form'] = render_to_string(template_name,
                                         context,
                                         request=request)
    return JsonResponse(data)


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
    else:
        form = ProjectForm()
    return save_form(request, form, 'projects/includes/partial_project_create.html')


def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
    else:
        form = ProjectForm(instance=project)
    return save_form(request, form, 'projects/includes/partial_project_update.html')


def task_create(request, project_pk):
    if request.method == "POST":
        form = TaskForm(request.POST)
        form.project = project_pk
        if form.is_valid():
            task = form.save(commit=False)
            project = get_object_or_404(Project, pk=project_pk)
            task.project = project
            task.save()

            data = dict()
            data['form_is_valid'] = True
            projects = Project.objects.all()
            data['html_project_list'] = render_to_string(
                'projects/includes/partial_project_list.html', {'projects': projects})
            context = {'form': form}
            data['html_form'] = render_to_string('projects/includes/partial_task_create.html',
                                                 context,
                                                 request=request)
            return JsonResponse(data)

    else:
        form = TaskForm()
        form.project = project_pk
        return save_form(request, form, 'projects/includes/partial_task_create.html')


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
    else:
        form = TaskForm(instance=task)
    return save_form(request, form, 'projects/includes/partial_task_update.html')


def task_toggle(request, pk):
    data = {}
    task = get_object_or_404(Task, pk=pk)
    print(task)
    if task:
        if task.completed == True:
            task.completed = False
        else:
            task.completed = True
        task.save()
        projects = Project.objects.all()
        data['html_project_list'] = render_to_string(
            'projects/includes/partial_project_list.html', {'projects': projects})
        return JsonResponse(data)

    data['status'] = 404
    return JsonResponse(data)
