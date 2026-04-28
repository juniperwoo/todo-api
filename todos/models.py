from django.db import models


class Todo(models.Model):
    class Priority(models.TextChoices): #defines fixed values for priority
        LOW    = 'low',    'Low' #stored in db as low, shown to user as Low
        MEDIUM = 'medium', 'Medium'
        HIGH   = 'high',   'High'

    title       = models.CharField(max_length=255)
    description = models.TextField(blank=True) #users can leave it empty
    completed   = models.BooleanField(default=False)
    priority    = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM) #
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta: #sets default order of todo as newest task first
        ordering = ['-created_at']

    def __str__(self):
        return self.title