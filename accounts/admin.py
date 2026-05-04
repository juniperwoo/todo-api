from django.contrib import admin #register models to admin panel
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin #to customize the user model in admin panel
from .models import User #importing the custom user model
from todos.models import Todo #to show todo inside user admin

class TodoInline(admin.TabularInline): #tabularinline display data in table format
    model          = Todo
    fields         = ('title', 'priority', 'completed')

@admin.register(User) #decorator to register the user model with the admin panel
class UserAdmin(BaseUserAdmin): #extend django's default user admin
    list_display    = ('id', 'username', 'email', 'is_active', 'is_staff', 'date_joined')
    list_filter     = ('is_active', 'is_staff', 'is_superuser')
    search_fields   = ('username', 'email')
    ordering        = ('-date_joined',)
    readonly_fields = ('created_at', 'updated_at')
    inlines         = [TodoInline] #shows their todo under each user