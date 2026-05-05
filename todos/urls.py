from django.urls import path
from . import views #imports views.py so we can call functions 
app_name = 'todos'
urlpatterns = [
 path('',                         views.web_todos,         name='list'),
    path('create/',               views.web_todo_create,   name='create'),
    path('<int:pk>/toggle/',       views.web_todo_toggle,   name='toggle'),
    path('<int:pk>/delete/',        views.web_todo_delete,   name='delete'),
    path('<int:pk>/edit/',           views.web_todo_edit,     name='edit'),
]