from django.urls import path
from . import views #imports views.py so we can call functions 
from .views import RegisterView, LoginView
urlpatterns = [
    # Auth API
    path('auth/register/', views.register,  name='register'),
    path('auth/login/',    views.login,     name='login'),
    path('auth/logout/',   views.logout,    name='logout'),
    path('auth/profile/',  views.profile,   name='profile'),
    path('auth/token/refresh/', views.token_refresh, name='token-refresh'),
    
    path('auth/register-raw/', RegisterView.as_view(), name='register-raw'),
    path('auth/login-raw/', LoginView.as_view(), name='login-raw'),

 #todos ko API
    path('todos/',             views.todo_list,   name='todo-list'),
    path('todos/<int:pk>/',    views.todo_detail, name='todo-detail'),
    path('todos/<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
]