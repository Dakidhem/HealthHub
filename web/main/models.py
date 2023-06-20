from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_TYPES = (
        ('Hospital', 'Hospital',),
        ('Doctor', 'Doctor')
        )
    user_type = models.CharField(max_length = 10, choices = USER_TYPES, default = USER_TYPES[0][0])
    hospital=models.ForeignKey('self', blank=True, null=True,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="doctors", blank=True, null=True)

class ContactMessage(models.Model):
    email = models.CharField(max_length = 100,blank=True, null = True)
    subject = models.CharField(max_length = 100,blank=True, null = True)
    message = models.TextField(blank=True, null = True)
    date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, related_name='contact_message', on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = "ContactMessages"
