from django.contrib import admin
from django.urls import path, include
from todos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('todos.urls')),

    # Web pages
    path('',          views.web_login,        name='web_login'),
    path('login/',    views.web_login,        name='web_login'),
    path('register/', views.web_register,     name='web_register'),
    path('logout/',   views.web_logout,       name='web_logout'),
    path('todos/',    views.web_todos,        name='web_todos'),
    path('todos/create/',        views.web_todo_create, name='web_todo_create'),
    path('todos/<int:pk>/toggle/', views.web_todo_toggle, name='web_todo_toggle'),
    path('todos/<int:pk>/delete/', views.web_todo_delete, name='web_todo_delete'),
    path('todos/<int:pk>/edit/',       views.web_todo_edit,   name='web_todo_edit'),
]