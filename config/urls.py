from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from todos import views as todo_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/auth/', include('accounts.urls')),
    path('api/',      include('todos.urls')),

    # Web pages
    path('',                               account_views.web_login,      name='web_login'),
    path('login/',                         account_views.web_login,      name='web_login'),
    path('register/',                      account_views.web_register,   name='web_register'),
    path('logout/',                        account_views.web_logout,     name='web_logout'),
    path('todos/',                         todo_views.web_todos,         name='web_todos'),
    path('todos/create/',                  todo_views.web_todo_create,   name='web_todo_create'),
    path('todos/<int:pk>/toggle/',         todo_views.web_todo_toggle,   name='web_todo_toggle'),
    path('todos/<int:pk>/delete/',         todo_views.web_todo_delete,   name='web_todo_delete'),
    path('todos/<int:pk>/edit/',           todo_views.web_todo_edit,     name='web_todo_edit'),
]