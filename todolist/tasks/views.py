from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskFile, Tag, TaskGroup
from .forms import TaskForm, TaskGroupForm


def index(request):
    form = TaskForm()
    tasks = Task.objects.all()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            if request.FILES.get('file'):
                TaskFile.objects.create(task=task, file_path=request.FILES['file'].name)
            return redirect('/')
    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks.html', context)


def updatetask(request, pk):
    task = get_object_or_404(Task, id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            form.save_m2m()
            if request.FILES.get('file'):
                TaskFile.objects.create(task=task, file_path=request.FILES['file'].name)
            return redirect('/')
    context = {'form': form}
    return render(request, 'update-tasks.html', context)


def deleteTask(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    context = {'task': task}
    return render(request, 'delete-task.html', context)
