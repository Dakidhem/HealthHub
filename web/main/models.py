from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass

class ContactMessage(models.Model):
    email = models.CharField(max_length = 100,blank=True, null = True)
    subject = models.CharField(max_length = 100,blank=True, null = True)
    message = models.TextField(blank=True, null = True)
    date = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, related_name='contact_message', on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = "ContactMessages"