"""
URL configuration for clinicA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Management.views import *
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="Home"),

    path('aboutus', aboutus_view),
    path('contactus', contactus_view),

   

    path('adminclick', admin_click_view, name="Admin"),
    path('doctorclick', doc_click_view, name="Docktor"),
    path('patientclick', patient_click_view, name="Patient"),


    path('adminsignup', admin_signup_view, name="AdminSignUp"),
    path('doctorsignup', doctor_signup_view, name="DoctorSignUp"),
    path('patientsignup', patient_signup_view, name="PatientSignUp"),



    path('adminlogin', LoginView.as_view(template_name='adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='patientlogin.html')),
    path('afterLogin', afterlogin_view, name="afterLogin"),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),


    path('admin-dashboard', admin_dashboard_view, name='admin-dashboard'),
    path('admin-doctor', admin_doctor_view, name='admin-doctor'),
    path('admin-view-doctor', admin_view_doctor_view, name='admin-view-doctor'),
    path('update-doctor/<int:id>', update_doctor_view,name='update-doctor'),
    path('delete-doctor-from-hospital/<int:id>', admin_delete_doctor_view, name='delete-doctor-from-hospital'),
    path('admin-add-doctor', admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-approve-doctor', admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:id>', approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', reject_doctor_view,name='reject-doctor'),
    path('admin-view-doctor-specialisation', admin_doctor_specialization_view,name='admin-view-doctor-specialisation'),


    path('admin-patient', admin_patient_view,name='admin-patient'),
    path('admin-view-patient', admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:id>', admin_delete_patient_view,name='delete-patient-from-hospital'),
    path('update-patient/<int:id>', admin_update_patient_view,name='update-patient'),
    path('admin-add-patient', admin_add_patient_view,name='admin-add-patient'),
    path('admin-approve-patient', admin_approve_patient_view,name='admin-approve-patient'),
    path('approve-patient/<int:id>', approve_patient_view,name='approve-patient'),
    path('reject-patient/<int:id>', reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:id>', discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:id>', download_pdf_view,name='download-pdf'),


    path('admin-appointment', admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:id>', approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:id>', reject_appointment_view,name='reject-appointment'),

    #------------------------------------Doctor Related URls-----------------------------------
    #------------------------------------------------------------------------------------------

    path('doctor-dashboard', doctor_dashboard_view,name='doctor-dashboard'),
    path('search', search_view,name='search'),
    path('doctor-patient', doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-discharge-patient',doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
    path('doctor-appointment', doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:id>', delete_appointment_view,name='delete-appointment'),
    path('get_timeslots', get_timeslots, name='get_timeslots'),
    path('add-report/<int:id>', doctor_add_report_view, name='add-report'),
    



    #-----------------------------------Patient Related Urls---------------------------------------
    #----------------------------------------------------------------------------------------------

    path('patient-dashboard', patient_dashboard_view,name='patient-dashboard'),
    path('patient-dashboard', patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor', search_doctor_view,name='searchdoctor'),
    path('patient-discharge', patient_discharge_view,name='patient-discharge'),
    
    
    
    ]
