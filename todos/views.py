from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from accounts.views import jwt_required
from .models import Todo



@jwt_required
def web_todos(request):
    todos = Todo.objects.filter(user=request.jwt_user)
    filter_param = request.GET.get('filter')
    if filter_param == 'active':
        todos = todos.filter(completed=False)
    elif filter_param == 'completed':
        todos = todos.filter(completed=True)
    elif filter_param == 'high':
        todos = todos.filter(priority='high')
    return render(request, 'todos/todos.html', {
        'todos': todos,
        'jwt_user': request.jwt_user,
    })


@jwt_required
def web_todo_create(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority    = request.POST.get('priority', 'medium')
        if title:
            Todo.objects.create(user=request.jwt_user, title=title, description=description, priority=priority)
            messages.success(request, 'Todo added!')
        else:
            messages.error(request, 'Title is required.')
    return redirect('todos:list')


@jwt_required
def web_todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.jwt_user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todos:list')


@jwt_required
def web_todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.jwt_user)
    todo.delete()
    messages.success(request, 'Todo deleted.')
    return redirect('todos:list')


@jwt_required
def web_todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.jwt_user)
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority    = request.POST.get('priority', 'medium')
        if title:
            todo.title       = title
            todo.description = description
            todo.priority    = priority
            todo.save()
            messages.success(request, 'Todo updated!')
        else:
            messages.error(request, 'Title is required.')
    return redirect('todos:list')