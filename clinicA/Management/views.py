from datetime import date, timedelta, time
import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from .forms import *
from .models import *

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request, 'index.html')



def admin_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request, 'adminclick.html')



def doc_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request, 'doctorclick.html')



def patient_click_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterLogin')
    return render(request, 'patientclick.html')



def admin_signup_view(request):
    form = adminSignUpForm()
    if request.method == 'POST':
        form = adminSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            admin_group = Group.objects.get_or_create(name='ADMIN')
            admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'adminsignup.html',{'form':form})



def doctor_signup_view(request):
     userform = docktorUserForm()
     doctorform = docktorForm()
     context = {
        'userForm': userform,
        'doctorForm': doctorform,
     }
     if request.method == 'POST':
        userform = docktorUserForm(request.POST)
        doctorform = docktorForm(request.POST, request.FILES)
        print('User Form Errors : ', userform.errors)
        if doctorform.is_valid() :
            print('Forms are Valid')
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor.workHours = request.POST.get('workHours')
            doctor.workDays = request.POST.getlist('workDays')
            doctor.workStart = request.POST.get('workStart')
            doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            return HttpResponseRedirect('doctorlogin')
     return render(request,'doctorsignup.html',context=context)



def patient_signup_view(request):
    userForm = patientUserForm()
    patientForm = PatientForm()
    context = {
        'userForm':userForm,
        'patientForm':patientForm,
        }
    if request.method == 'POST':
        print (request.POST.get('assignedDoctor_id'))
        doctor = get_object_or_404(Doctor, user_id=request.POST.get('assignedDoctor_id'))
        userForm = patientUserForm(request.POST)
        patientForm = PatientForm(request.POST, request.FILES)
        print('Form Errors : ', patientForm.errors)
        if userForm.is_valid() and patientForm.is_valid():
            print('Forms are Valid')
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.assignedDoctor_id = doctor
            patient = patient.save()
            patient_group = Group.objects.get_or_create(name='PATIENT')
            patient_group[0].user_set.add(user)
            return HttpResponseRedirect('patientlogin')
    return render(request,'patientsignup.html',context=context)



# For Checking user is Admin, Doctor, patient
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()



def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()



def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


# After Entering Credintials we check if user is in Admin, Doctor, Patient Groups
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountApproval = Doctor.objects.all().filter(user_id=request.user.id, status=True)
        if accountApproval:
            return redirect('doctor-dashboard')
        else :
            return render(request, 'doctor_wait_for_approval.html')
    elif is_patient(request.user):
        accountApproval = Patient.objects.all().filter(user_id=request.user.id, status=True)
        if accountApproval :
            return redirect('patient-dashboard')
        else :
            return render(request, 'patient_wait_for_approval.html')
        


# -----------------------Admin Related Views Starts----------------------
#------------------------------------------------------------------------

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
# For Both Tables in Admin Dashboard
    doctors = Doctor.objects.all().order_by('-id')
    patients = Patient.objects.all().order_by('-id')

# For Three Cards 
    doctorCount = Doctor.objects.all().filter(status=True).count()
    pendingDoctorCount = Doctor.objects.all().filter(status=False).count()

    patientCount = Patient.objects.all().filter(status=True).count()
    pendingPatientCount = Patient.objects.all().filter(status=False).count()

    appointmentCount = Appointment.objects.all().filter(status=True).count()
    pendingAppointmentCount =   Appointment.objects.all().filter(status=False,passed=False).count()

    dict = {
        'doctors': doctors,
        'patients': patients,
        'doctorcount':doctorCount,
        'pendingdoctorcount':pendingDoctorCount,
        'patientcount':patientCount,
        'pendingpatientcount':pendingPatientCount,
        'appointmentcount':appointmentCount,
        'pendingappointmentcount':pendingAppointmentCount,
    }


    return render(request,'admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors = Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_doctor_view(request,id):
    doctor = Doctor.objects.get(id=id)
    user = User.objects.get(id = doctor.user.id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,id):
    doctor = Doctor.objects.get(id=id)
    user = User.objects.get(id = doctor.user.id)
    userform = docktorUserForm(instance=user)
    doctorform = docktorForm(request.FILES, instance=doctor)
    dict = {
        'userForm': userform,
        'doctorForm':doctorform
    }

    if request.method == 'POST':
        userform = docktorUserForm(request.POST, instance=user)
        doctorform = docktorForm(request.POST, request.FILES, instance=doctor)
        if userform.is_valid() and doctorform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorform.save(commit=False)
            doctor.workHours = request.POST.get('workHours')
            doctor.workDays = request.POST.getlist('workDays')
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'admin_update_doctor.html',context=dict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userform = docktorUserForm()
    doctorform = docktorForm()
    dict = {
        'userForm': userform,
        'doctorForm': doctorform
    }
    if request.method == 'POST':
        userform = docktorUserForm(request.POST)
        doctorform = docktorForm(request.POST, request.FILES)
        if userform.is_valid() and doctorform.is_valid() :
            user = userform.save()
            user.set_password(user.password)
            user.save()
            doctor = doctorform.save(commit=False)
            doctor.user = user
            doctor.status = True
            doctor.workHours = request.POST.get('workHours')
            doctor.workDays = request.POST.getlist('workDays')
            doctor.workStart= request.POST.get('workStart')
            doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-doctor')
    return render(request,'admin_add_doctor.html',context=dict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    doctors = Doctor.objects.all().filter(status = False)
    return render(request,'admin_approve_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request, id):
    doctor = Doctor.objects.get(id=id)
    doctor.status = True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request, id):
    doctor = Doctor.objects.get(id=id)
    user = User.objects.get(id = doctor.user.id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_specialization_view(request):
    doctors = Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctor_specialisation.html',{'doctors':doctors})
#--------------------------------------Admin Patient View --------------------------------
#-----------------------------------------------------------------------------------------


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients = Patient.objects.all().filter(status=True)
    return render(request,'admin_view_patient.html',{'patients':patients})




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_delete_patient_view(request, id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id = patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_update_patient_view(request, id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id = patient.user_id)
    userform = patientUserForm(instance=user)
    patientform = PatientForm(request.FILES, instance=patient)
    dict = {
            'userForm': userform,
            'patientForm': patientform
        }

    if request.method == 'POST':
        userform = patientUserForm(request.POST,instance=user)
        patietform = PatientForm(request.POST, request.FILES, instance=patient)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            patient = patientform.save(commit=False)
            patient.status = True
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request, 'admin_update_patient.html',context=dict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userform = patientUserForm()
    patientform = PatientForm()
   
    context = {
        'userForm': userform,
        'patientForm': patientform
    }

    if request.method == 'POST':
        patientform = PatientForm(request.POST, request.FILES)
        userform = patientUserForm(request.POST)
        print('patient Form Errors', patientform.errors)
        print('user Form Errors', userform.errors)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            patient = patientform.save(commit=False)
            patient.user = user
            patient.status = True
            print(request.POST.get('assignedDoctor_id'))
            patient.assignedDoctor_id = get_object_or_404(Doctor, user_id=request.POST.get('assignedDoctor_id'))
            patient.save()
            patient_group = Group.objects.get_or_create(name='PATIENT')
            patient_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-patient')
    return render(request,'admin_add_patient.html',context=context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    patients = Patient.objects.all().filter(status=False)
    return render(request,'admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request, id):
    patient = Patient.objects.get(id=id)
    patient.status = True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request, id):
    patient = Patient.objects.get(id=id)
    user = User.objects.get(id=patient.user_id)
    patient.delete()
    user.delete()
    return redirect('admin-approve-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients = Patient.objects.all().filter(status=True)
    return render(request,'admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,id):
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



#------------------------- For PatientDischarging PDF & Printing --------------------------------
#------------------------------------------------------------------------------------------------

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,id):
    patient = Patient.objects.get(id=id)
    dischargeDetails=PatientDischargeDetails.objects.all().filter(patient=patient).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patient,
        'assignedDoctorName':dischargeDetails[0].doctor,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('download_bill.html',dict)



#-----------------------------------------Apointment Starts---------------------------------
#-------------------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=Appointment.objects.all().filter(status=True)
    return render(request,'admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointment_form = AppointmentForm()
    context = {
        'appointmentForm': appointment_form,
    }
    if request.method == 'POST':
        appointment_form = AppointmentForm(request.POST)
        if appointment_form.is_valid():
            appointment = appointment_form.save(commit=False)
            doctor = get_object_or_404(Doctor, user_id=request.POST.get('doctorId'))
            patient = get_object_or_404(Patient, user_id=request.POST.get('patientId'))
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.date = appointment_form.cleaned_data['date']
            appointment.time = appointment_form.cleaned_data['time']
            appointment.status = True
            appointment.save()
            return HttpResponseRedirect('admin-view-appointment')
    return render(request,'admin_add_appointment.html',context=context)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=Appointment.objects.all().filter(status=False, passed=False)
    return render(request,'admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.status = True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request, id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect('admin-approve-appointment')



#--------------------------------Doctor Related Views Starts------------------------------------
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    # For Three Cards 
    doctor = get_object_or_404(Doctor,user=request.user)
    patientCount = Patient.objects.all().filter(status=True, assignedDoctor_id=doctor).count()
    appointmentCount = Appointment.objects.all().filter(status=True, doctor=doctor, passed=False).count()
    patientdischarged = PatientDischargeDetails.objects.all().distinct().filter(doctor=doctor).count()

    # For table in Doctor Dashboard 
    appointments = Appointment.objects.all().filter(status=True, doctor=doctor).order_by('-id')
    patientid = []
    for a in appointments:
        patientid.append(a.patient.user_id)
    patients = Patient.objects.all().filter(status=True, user_id__in=patientid).order_by('-id')
    appointments = zip(appointments, patients)
    mydict={
    'patientcount':patientCount,
    'appointmentcount':appointmentCount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict = {
        'doctor': Doctor.objects.get(user_id=request.user.id),
    }
    return render(request,'doctor_patient.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    doctor = get_object_or_404(Doctor,user_id=request.user.id)
    patients = Patient.objects.all().filter(status=True, assignedDoctor_id=doctor)
    doctor = Doctor.objects.get(user_id = request.user.id)
    return render(request,'doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor = Doctor.objects.get(user_id = request.user.id)
    query = request.GET['query']
    patients = Patient.objects.all().filter(status=True, assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    doctor = get_object_or_404(Doctor,user_id=request.user.id)
    dischargePatients = PatientDischargeDetails.objects.all().distinct().filter(doctor=doctor)
    return render(request,'doctor_view_discharge_patient.html',{'dischargedpatients':dischargePatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor = Doctor.objects.get(user_id=request.user.id)
    return render(request,'doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = get_object_or_404(Doctor,user_id=request.user.id)
    appointments = Appointment.objects.all().filter(status=True,doctor=doctor, passes=False)
    doctor = Doctor.objects.get(user_id=request.user.id)
    patientId = []
    for a in appointments:
        patientId.append(a.patient.user_id)
    patients = Patient.objects.all().filter(status=True,user_id__in=patientId)
    appointments = zip(appointments,patients)
    return render(request,'doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor = get_object_or_404(Doctor,user_id=request.user.id)
    appointments = Appointment.objects.all().filter(status=True, doctor=doctor)
    doctor = Doctor.objects.get(user_id=request.user.id)
    patientId = []
    for a in appointments:
        patientId.append(a.patient.user_id)
    patients = Patient.objects.all().filter(status=True, user_id__in=patientId)
    appointments = zip(appointments,patients)
    return render(request,'doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,id):
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    doctor = Doctor.objects.get(user_id=request.user.id)
    appointments=Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

    

def get_timeslots(request):
    doctor_id = int(request.GET.get('doctorId'))
    doctor = get_object_or_404(Doctor, user_id=doctor_id)
    date_str = request.GET.get('date')
    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    print('Date is: ', date)

    work_start = doctor.workStart
    work_start_datetime = datetime.datetime.combine(date, work_start)
    print('Work Starts At:', work_start_datetime)
    work_hours = doctor.workHours
    work_ends = work_start_datetime + timedelta(hours=work_hours)

    reserved_appointments = Appointment.objects.filter(doctor=doctor, date=date, passed=False)
    reserved_timeslots = [appointment.time for appointment in reserved_appointments]
    print('Reserved Time Slots are:', reserved_timeslots)

    available_timeslots = []
    current_time = work_start_datetime
    while current_time + timedelta(minutes=30) <= work_ends:
        if current_time.time() not in reserved_timeslots:
            available_timeslots.append(current_time.time())
        current_time += timedelta(minutes=30)
    print('Available Time Slots are:', available_timeslots)

    return JsonResponse([time.strftime('%H:%M') for time in available_timeslots], safe=False)


def doctor_add_report_view(request,id):  
    report_form = AddReport() 
    appointment = get_object_or_404(Appointment, pk=id)
    if request.method == 'POST':
        report_form=AddReport(request.POST)
        print('Form Errors : ', report_form.errors)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            print('Report is : ',request.POST.get('patientReport'))
            appointment.patientReport = report.patientReport
            appointment.passed = True
            appointment.save()
            return redirect('doctor-view-appointment')
    return render(request, 'doctor_add_report.html',{'report_form': report_form})



def doctor_view_patient_history(request,id):
    patient = get_object_or_404(Patient, pk=id)
    appointments = Appointment.objects.all().filter(patient=patient)
    doctor = patient.assignedDoctor_id
    return render(request, 'doctor_view_patient_history.html',{'appointments':appointments,'doctor':doctor})
    









#----------------------------------------Patient Related Views Starts---------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient = Patient.objects.get(user_id=request.user.id)
    doctor = Doctor.objects.get(user_id=patient.assignedDoctor_id.user_id)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'patient_dashboard.html',context=mydict)
    


@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient = Patient.objects.get(user_id=request.user.id) 
    return render(request,'patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm = PatientAppointmentForm()
    patient = Patient.objects.get(user_id=request.user.id) 
    message = None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm = PatientAppointmentForm(request.POST)
        print('Appointment Form Errors : ',appointmentForm.errors)
        if appointmentForm.is_valid():
            print('doctor ID is: ',request.POST.get('doctorId'))
            print('Date is :', request.POST.get('Date'))
            print('Time is : ', request.POST.get('Time'))
            doctor = get_object_or_404(Doctor, user_id=request.POST.get('doctorId'))
            date = appointmentForm.cleaned_data['date']
            time = appointmentForm.cleaned_data['time']
            appointment = appointmentForm.save(commit=False)
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.date =  date
            appointment.time = time 
            appointment.status=False
            appointment.save()
            return HttpResponseRedirect('patient-view-appointment')
    
    return render(request,'patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors = Doctor.objects.all().filter(status=True)
    patient = Patient.objects.get(user_id=request.user.id) 
    return render(request,'patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient = Patient.objects.get(user_id=request.user.id)
    query = request.GET['query']
    doctors = Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'patient_view_doctor.html',{'patient':patient,'doctors':doctors})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient = Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments = Appointment.objects.all().filter(patient=patient)
    return render(request,'patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient = Patient.objects.get(user_id=request.user.id) 
    dischargeDetails = PatientDischargeDetails.objects.all().filter(patient=patient).order_by('-id')[:1]
    patientDict = None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.user_id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient_discharge.html',context=patientDict)

#----------------------------------------------------------------------------
#----------------------------------------------------------------------------

def aboutus_view(request):
    return render(request,'aboutus.html')

def contactus_view(request):
    sub = ContactusForm()
    if request.method == 'POST':
        sub = ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})





#-------------------------------------------------------------------
#------------------------When Apointment Time Ends------------------
def appointment_time_end():
    current_date = datetime.datetime.date()
    appointments = Appointment.objects.all()
    for appointment in appointments:
        if appointment.date < current_date :
            appointment.passed = True
            appointment.status = False
            appointment.save()








