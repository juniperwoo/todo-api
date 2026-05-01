from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from accounts.views import jwt_required
from .models import Todo
from .serializers import TodoSerializer


# API Todo Views

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todo_list(request):
    if request.method == 'GET':
        todos = Todo.objects.filter(user=request.user)
        completed = request.query_params.get('completed')
        if completed is not None:
            todos = todos.filter(completed=completed.lower() == 'true')
        priority = request.query_params.get('priority')
        if priority:
            todos = todos.filter(priority=priority)
        serializer = TodoSerializer(todos, many=True)
        return Response({'count': todos.count(), 'results': serializer.data})

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'GET':
        return Response(TodoSerializer(todo).data)
    elif request.method == 'PATCH':
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        todo.delete()
        return Response({'message': 'Todo deleted.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return Response(TodoSerializer(todo).data)


# Web Todo Views

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
    return redirect('web_todos')


@jwt_required
def web_todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.jwt_user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('web_todos')


@jwt_required
def web_todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.jwt_user)
    todo.delete()
    messages.success(request, 'Todo deleted.')
    return redirect('web_todos')


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
    return redirect('web_todos')