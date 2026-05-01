from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    class Priority(models.TextChoices): #defines fixed values for priority
        LOW    = 'low',    'Low' #stored in db as low, shown to user as Low
        MEDIUM = 'medium', 'Medium'
        HIGH   = 'high',   'High'

    #yo user=1 wala
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True) #users can leave it empty
    completed   = models.BooleanField(default=False)
    #no need for max length here
    priority    = models.CharField(choices=Priority.choices, default=Priority.MEDIUM) #
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta: #sets default order of todo as newest task first
        ordering = ['-created_at']

    
    #def __str__(self):
       # return f"{self.user.username} - {self.title}" this was making django to go to db and fetch full user obj and also expose username

    def __str__(self):
     return f"Todo({self.id}) - {self.title} [user:{self.user_id}]"