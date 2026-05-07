from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings 

@shared_task
def send_welcome_email(username, email):
    subject = 'Welcome to our todo application!!!'
    message= f'''
    Hi {username} :),
    Welcome to our todo application. We are glad to have you on our platform hehe. Your account has been successfully created!!
    You can now login and start creating & managing your todos at:
    http://localhost:8000/

    best regards,
    the todo app team
    '''
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently= False, 
    )
    

