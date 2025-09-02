from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskFile, CustomUser
from .forms import TaskForm
from django.db.models import Q


def get_logged_user(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None
    return None


def user_login(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomUser.objects.filter(email=email, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return redirect('task-list')
        else:
            error = 'Email ou senha inválidos.'
    return render(request, 'login.html', {'error': error})


def user_register(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            error = 'Email já cadastrado.'
        else:
            CustomUser.objects.create(email=email, password=password)
            return redirect('login')
    return render(request, 'register.html', {'error': error})


def user_logout(request):
    request.session.flush()
    return redirect('login')


def task_list(request):
    user = get_logged_user(request)
    if not user:
        return redirect('login')
    order = request.GET.get('order', 'recent')
    search = request.GET.get('search', '').strip()
    tasks = Task.objects.filter(user=user)
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
    user = get_logged_user(request)
    if not user:
        return redirect('login')
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            form.save_m2m()
            if request.FILES.get('file'):
                TaskFile.objects.create(task=task, file_path=request.FILES['file'].name)
            return redirect('task-list')
    return render(request, 'task_create.html', {'form': form})


def task_update(request, pk):
    user = get_logged_user(request)
    if not user:
        return redirect('login')
    task = get_object_or_404(Task, id=pk, user=user)
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
    user = get_logged_user(request)
    if not user:
        return redirect('login')
    task = get_object_or_404(Task, id=pk, user=user)
    if request.method == 'POST':
        task.delete()
        return redirect('task-list')
    return render(request, 'task_delete.html', {'task': task})
