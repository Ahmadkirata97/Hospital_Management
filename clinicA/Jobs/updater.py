from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from apscheduler.schedulers.background import BackgroundScheduler
from Jobs.jobs import *

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(appointment_time_end, 'interval', minutes=30)  # Adjust the interval as needed
    register_events(scheduler)
    scheduler.start()