import os
from celery import Celery
from kombu import Queue, Exchange
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clinicA.settings')
app = Celery("clinicA")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks',
          queue_arguments={'x-max-priority': 10}),
]

app.conf.task_acks_late = True # Sets the late Ack of tasks, execute the task then send Ack 
app.conf.task_default_priority = 5
app.conf.worker_prefetch_multiplier = 1 # enable the worker to fetch multiple tasks from the broker at once 
app.conf.worker_concurrency = 1 # number of worker threds that celery will reserve to process task 

# base_dir = os.getcwd()
# task_folder = os.path.join(base_dir,'Management')
# if os.path.exists(task_folder) and os.path.isdir(task_folder):
#     task_modules = []
#     for filename in os.listdir(task_folder):
#         if filename == 'tasks.py':
#             module_name = 'Management.tasks'
#             module = __import__(module_name, fromlist=['*'])
#             for name in dir(module):
#                 obj = getattr(module, name)
#                 if callable(obj):
#                     task_modules.append(f'{module_name}.{name}')
#     app.autodiscover_tasks(task_modules)