import os 
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') #sets the default Django settings module for the 'celery' program to 'config.settings', ensuring that Celery can access the Django settings when it runs tasks.

app = Celery('config') 

app.config_from_object('django.conf:settings', namespace= 'CELERY') #configures the Celery app to read its settings from the Django settings module, using the 'celery' namespace to identify relevant settings
app.autodiscover_tasks() #tells Celery to automatically discover tasks defined in Django apps by looking for a 'tasks.py' file in each app directory
 