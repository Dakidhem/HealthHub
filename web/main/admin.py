from django.contrib import admin

from .models import *

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('user','email','subject','message')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email','user_type','hospital')

admin.site.register(User,UserAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
# Register your models here.
