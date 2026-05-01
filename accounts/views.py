import re
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings as django_settings
from .serializers import RegisterSerializer, UserSerializer


# Helpers

def set_jwt_cookies(response, access_token, refresh_token):
    response.set_cookie(
        django_settings.JWT_ACCESS_COOKIE,
        str(access_token),
        max_age=60 * 30,
        httponly=True,
        samesite='Lax',
    )
    response.set_cookie(
        django_settings.JWT_REFRESH_COOKIE,
        str(refresh_token),
        max_age=60 * 60 * 24 * 7,
        httponly=True,
        samesite='Lax',
    )
    return response


def get_user_from_cookie(request):
    from rest_framework_simplejwt.tokens import AccessToken
    token = request.COOKIES.get(django_settings.JWT_ACCESS_COOKIE)
    if not token:
        return None
    try:
        decoded = AccessToken(token)
        user_id = decoded['user_id']
        return User.objects.get(id=user_id)
    except Exception:
        return None


def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = get_user_from_cookie(request)
        if not user:
            return redirect('web_login')
        request.jwt_user = user
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# API Auth Views

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user':    UserSerializer(user).data,
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
        'user':    UserSerializer(user).data,
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


# Web Auth Views

def web_login(request):
    if get_user_from_cookie(request):
        return redirect('web_todos')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh  = RefreshToken.for_user(user)
            response = redirect('web_todos')
            set_jwt_cookies(response, refresh.access_token, refresh)
            return response
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'todos/login.html')


def web_register(request):
    if get_user_from_cookie(request):
        return redirect('web_todos')
    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email', '')
        password  = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        elif not re.search(r'[A-Z]', password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
        elif not re.search(r'[a-z]', password):
            messages.error(request, 'Password must contain at least one lowercase letter.')
        elif not re.search(r'[0-9]', password):
            messages.error(request, 'Password must contain at least one number.')
        elif not re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
            messages.error(request, 'Password must contain at least one special character.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user     = User.objects.create_user(username=username, email=email, password=password)
            refresh  = RefreshToken.for_user(user)
            response = redirect('web_todos')
            set_jwt_cookies(response, refresh.access_token, refresh)
            return response
    return render(request, 'todos/register.html')


def web_logout(request):
    response = redirect('web_login')
    response.delete_cookie(django_settings.JWT_ACCESS_COOKIE)
    response.delete_cookie(django_settings.JWT_REFRESH_COOKIE)
    return response