import re #used for password validation 
from rest_framework_simplejwt.tokens import RefreshToken #generates access and refresh token
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings as django_settings
from .models import User

# Helpers

def set_jwt_cookies(response, access_token, refresh_token): #stores 2 tokens in browser cookies for protection and expiry mgmt
    response.set_cookie(
        django_settings.JWT_ACCESS_COOKIE,
        str(access_token),
        max_age=60 * 30, 
        httponly=True,
        samesite='Lax', #prevents CSRF attacks by not sending cookies on cross-site requests, but allows them on same-site requests.
        path='/',
    )
    response.set_cookie(
        django_settings.JWT_REFRESH_COOKIE,
        str(refresh_token),
        max_age=60 * 60 * 24 * 7, 
        httponly=True,
        samesite='Lax',
        path='/',
    )
    return response


def get_user_from_cookie(request): #extracts access token from cookie, decodes it to get user id, and retrieves user from database. 
    from rest_framework_simplejwt.tokens import AccessToken
    from accounts.models import User
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


# Web Auth Views

def web_login(request):
    if get_user_from_cookie(request):
        return redirect('todos:list')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh  = RefreshToken.for_user(user)
            response = redirect('todos:list')
            set_jwt_cookies(response, refresh.access_token, refresh)
            return response
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'todos/login.html')


def web_register(request):
    if get_user_from_cookie(request):
        return redirect('todos:list')
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
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
        else:
            user     = User.objects.create_user(username=username, email=email, password=password)
            refresh  = RefreshToken.for_user(user)
            response = redirect('todos:list')
            set_jwt_cookies(response, refresh.access_token, refresh)
            return response
    return render(request, 'todos/register.html')


def web_logout(request):
    response = redirect('web_login')
    response.delete_cookie(django_settings.JWT_ACCESS_COOKIE)
    response.delete_cookie(django_settings.JWT_REFRESH_COOKIE)
    return response