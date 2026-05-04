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
    path('',       account_views.web_login,      name='web_login'),
    path('auth/', include ('accounts.web_urls')),
    path('todos/', include('todos.web_urls')),
]