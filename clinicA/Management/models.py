import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import DateTimeField
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator






departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

workDaysChoices = (
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    )

defaultTime = 10


# Create your models here.


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=False, null=False, upload_to='profile_pic/DoctorProfilePic/')
    workHours = models.IntegerField(null=False, blank=False, validators=[MaxValueValidator(6)])
    workStart = models.TimeField(null=False,default=datetime.time(10,0))
    workDays = MultiSelectField(max_length=100, choices=workDaysChoices)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=False)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    
    @property
    def get_id(self):
        return self.user.id
    

    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)





class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    admitDate = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)


    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    

    @property
    def get_id(self):
        return self.user.id
    

    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"
    






class Appointment(models.Model):
    patient = models.OneToOneField(Patient,on_delete=models.CASCADE)
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    time = models.TimeField(null = False, blank = False)
    date = models.DateField(null = False, blank = False)
    description = models.TextField(max_length=500)
    patientReport = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.patient.name}'s Appointment on {self.date}"




class PatientDischargeDetails(models.Model):
    patient = models.OneToOneField(Patient,on_delete=models.CASCADE)
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE, null=True)
    admitDate = models.DateField(null=False)
    releaseDate = models.DateField(null=False)
    daySpent = models.PositiveIntegerField(null=False)
    roomCharge = models.PositiveIntegerField(null=False)
    medicineCost = models.PositiveIntegerField(null=False)
    doctorFee = models.PositiveIntegerField(null=False)
    OtherCharge = models.PositiveIntegerField(null=False)
    total = models.PositiveIntegerField(null=False)



