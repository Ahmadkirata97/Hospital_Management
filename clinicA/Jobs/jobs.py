from Management.models import *
import datetime


def appointment_time_end():
    print('Hello From Scheduler')
    current_date = datetime.datetime.now().date()
    appointments = Appointment.objects.all()
    for appointment in appointments:
        print(appointment)
        print(appointment.date < current_date)
        print('Appointment Date is : ',appointment.date)
        print('Current Date is : ',current_date)
        appointment_date = datetime.datetime.strptime(appointment.date.strftime("%Y-%m-%d"), "%Y-%m-%d").date()
        if appointment_date < current_date :
            appointment.passed = True
            appointment.status = False
            appointment.save()
