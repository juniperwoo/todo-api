from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       account_views.web_login,      name='web_login'),
    path('auth/', include ('accounts.urls')),
    path('todos/', include('todos.urls')),
]