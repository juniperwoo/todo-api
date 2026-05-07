from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_todo_reminder(todo_id):
    from .models import Todo

    try:
        todo = Todo.objects.get(id = todo_id)
    except Todo.DoesNotExist: #if todo absent, safely exit wo error cause bg task should never crash
            return

    if todo.completed:
        return

    user = todo.user
    email = user.email

    if not email:
        return   

    subject = f'Reminder: "{todo.title}" is still incomplete man!' #email subject includes the title of the todo
    message= f'''
    Hi {user.username},
     Welcomeee to our todo application. This is a reminder for your pending todo after 30 minutes, please complete it on time without any further delays.
    These are the details of your todo:
    Title: {todo.title}
    Description: {todo.description}
    Priority: {todo.priority}
    Created: {todo.created_at.strftime('%Y-%m-%d %H:%M')}

    Login to complete your todo at:
    http://localhost:8000/todos/

    you can complete the tasks dw ;)
    The todo app 
    '''
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently= False, ) 
        

