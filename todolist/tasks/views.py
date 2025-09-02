from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskFile
from .forms import TaskForm


def task_list(request):
    order = request.GET.get('order', 'recent')
    search = request.GET.get('search', '').strip()
    tasks = Task.objects.all()
    if search:
        tasks = tasks.filter(name__icontains=search)
    if order == 'recent':
        tasks = tasks.order_by('-created_at')
    elif order == 'oldest':
        tasks = tasks.order_by('created_at')
    elif order == 'alpha':
        tasks = tasks.order_by('name')
    elif order == 'urgency':
        tasks = tasks.order_by('-urgency_level')

    urgency_map = {
        'baixa': {'color': '#3cb371', 'icon': '🟢'},
        'media': {'color': '#ffd700', 'icon': '🟡'},
        'alta': {'color': '#ff8c00', 'icon': '🟠'},
        'urgente':{'color': '#ff3b3b', 'icon': '🔴'},
    }
    for t in tasks:
        u = urgency_map.get(t.urgency_level, {'color': '#222', 'icon': '⚪'})
        t.urgency_color = u['color']
        t.urgency_icon = u['icon']

    return render(request, 'tasks_list.html', {'tasks': tasks, 'order': order, 'search': search})


def task_create(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save()
            if request.FILES.get('file'):
                TaskFile.objects.create(task=task, file_path=request.FILES['file'].name)
            return redirect('task-list')
    return render(request, 'task_create.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            task = form.save()
            if request.FILES.get('file'):
                TaskFile.objects.create(task=task, file_path=request.FILES['file'].name)
            return redirect('task-list')
    return render(request, 'task_update.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task-list')
    return render(request, 'task_delete.html', {'task': task})
