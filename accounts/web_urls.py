from django.urls import path
from . import views

urlpatterns = [
    path('login/',       views.web_login,      name='web_login'),
    path('register/',     views.web_register,   name='web_register'),
    path('logout/',      views.web_logout,     name='web_logout'),
   
]