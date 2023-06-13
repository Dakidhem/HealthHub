from django.contrib import admin
from .models import Patient, XrayImage

class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


admin.site.register(Patient)
admin.site.register(XrayImage)
