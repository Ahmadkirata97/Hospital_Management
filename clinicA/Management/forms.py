from datetime import date
import time
from typing import Self
from django import forms
from django.contrib.auth.models import User
from .models import *

class adminSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {
            'password': forms.PasswordInput()
        }



class docktorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {
            'password': forms.PasswordInput()
        }

class docktorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields=['address','mobile','department','status','profile_image','workHours','workDays','workStart']



class patientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','password']
        widgets = {
            'password': forms.PasswordInput()
        }


class PatientForm(forms.ModelForm):
    assignedDoctor_id=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model = Patient
        fields = ['address','mobile','status','symptoms','profile_image',]




class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
    class Meta:
        model=Appointment
        fields=['description','status']



class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=Appointment
        fields=['description','status']



class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))