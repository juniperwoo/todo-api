from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',       views.web_login,      name='login'),
    path('register/',     views.web_register,   name='register'),
    path('logout/',      views.web_logout,     name='logout'),
   
]