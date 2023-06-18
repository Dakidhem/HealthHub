from django.db import models
from main.models import User
from datetime import date

# Create your models here.


class Patient(models.Model):

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    BLOOD_TYPE_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    def __str__(self):
        return self.full_name

    full_name = models.CharField(max_length=200, blank=False, null=False)
    birth_date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='patients', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="patients", blank=True, null=True)
    description = models.TextField()
    phone_number = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, null=True, blank=True)
    adress = models.CharField(max_length=200, null=True, blank=True)
    archived=models.BooleanField(default=False)

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class XrayImage(models.Model):
    type_choices=(
        ("multiclass","multiclass"),
        ("pneumonia","pneumonia")
    )
    patient = models.ForeignKey(Patient, related_name='xray_images', on_delete=models.CASCADE)
    diagnostic = models.CharField(max_length=200, null=True, blank=True)
    xray_image = models.ImageField(upload_to="xray_images", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=type_choices,default=type_choices[0][0])