from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo
from .serializers import TodoSerializer, RegisterSerializer, UserSerializer


#API Auth Views

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide username and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'access':  str(refresh.access_token),
        'refresh': str(refresh),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully.'})
    except Exception:
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    return Response(UserSerializer(request.user).data)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        return Response({'access': str(token.access_token)})
    except Exception:
        return Response({'error': 'Invalid or expired refresh token.'}, status=status.HTTP_401_UNAUTHORIZED)


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


# Web Views

def web_login(request):
    if request.user.is_authenticated:
        return redirect('web_todos')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('web_todos')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'todos/login.html')


def web_register(request):
    if request.user.is_authenticated:
        return redirect('web_todos')
    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email', '')
        password  = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            auth_login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('web_todos')
    return render(request, 'todos/register.html')


def web_logout(request):
    auth_logout(request)
    return redirect('web_login')


@login_required
def web_todos(request):
    todos = Todo.objects.filter(user=request.user)
    filter_param = request.GET.get('filter')
    if filter_param == 'active':
        todos = todos.filter(completed=False)
    elif filter_param == 'completed':
        todos = todos.filter(completed=True)
    elif filter_param == 'high':
        todos = todos.filter(priority='high')
    return render(request, 'todos/todos.html', {'todos': todos})


@login_required
def web_todo_create(request):
    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        priority    = request.POST.get('priority', 'medium')
        if title:
            Todo.objects.create(user=request.user, title=title, description=description, priority=priority)
            messages.success(request, 'Todo added!')
        else:
            messages.error(request, 'Title is required.')
    return redirect('web_todos')


@login_required
def web_todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('web_todos')


@login_required
def web_todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    messages.success(request, 'Todo deleted.')
    return redirect('web_todos')

@login_required
def web_todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
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