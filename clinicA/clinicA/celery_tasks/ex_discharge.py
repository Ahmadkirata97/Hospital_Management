from clinicA.celery_conf import app
from Management.models import Patient
from django.shortcuts import render, redirect, reverse, get_object_or_404
from datetime import date, timedelta, time

@app.task(queue='tasks')
def discharge_patient_view_celery(request,id):
    patient=Patient.objects.get(id=id)
    print('patient User ID Is : ', patient.user_id)
    print('Assigned Doctor ID is : ', patient.assignedDoctor_id)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    doctor = get_object_or_404(Doctor, user=patient.assignedDoctor_id.user)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':id,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':doctor.user.first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=PatientDischargeDetails()
        pDD.patient=patient
        pDD.doctor=doctor
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'patient_final_bill.html',context=patientDict)
    return render(request,'patient_generate_bill.html',context=patientDict)
