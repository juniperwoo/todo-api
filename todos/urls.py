from django.urls import path
from . import views #imports views.py so we can call functions 
urlpatterns = [

 #todos ko API
    path('todos/',             views.todo_list,   name='todo-list'),
    path('todos/<int:pk>/',    views.todo_detail, name='todo-detail'),
    path('todos/<int:pk>/toggle/', views.todo_toggle, name='todo-toggle'),
]