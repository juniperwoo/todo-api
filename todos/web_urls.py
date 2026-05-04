from django.urls import path
from . import views

urlpatterns = [
     path('',                         views.web_todos,         name='web_todos'),
    path('create/',               views.web_todo_create,   name='web_todo_create'),
    path('<int:pk>/toggle/',       views.web_todo_toggle,   name='web_todo_toggle'),
    path('<int:pk>/delete/',        views.web_todo_delete,   name='web_todo_delete'),
    path('<int:pk>/edit/',           views.web_todo_edit,     name='web_todo_edit'),
]
