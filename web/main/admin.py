from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('user','email','subject','message')

admin.site.register(User,UserAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
# Register your models here.
