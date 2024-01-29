from clinicA.celery_conf import app
from Management.models import *
from django.shortcuts import render, redirect, reverse, get_object_or_404
from datetime import date, timedelta, time

@app.task(queue='tasks')
def discharge_patient_view_post(id,feeDict,medicineCost,OtherCharge,roomCharge,doctorFee,total):
    patient = Patient.objects.get(id=id)
    doctor = patient.assignedDoctor_id
    pDD=PatientDischargeDetails()
    pDD.patient=patient
    pDD.doctor=doctor
    pDD.admitDate=patient.admitDate
    pDD.releaseDate=date.today()
    pDD.daySpent=int(id)
    pDD.medicineCost=medicineCost
    pDD.roomCharge=roomCharge
    pDD.doctorFee=doctorFee
    pDD.OtherCharge=OtherCharge
    pDD.total=total
    pDD.save()
    return 