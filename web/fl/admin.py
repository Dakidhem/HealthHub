from django.contrib import admin

from .models import *

class FlResultsAdmin(admin.ModelAdmin):
    list_display = ('date','logs','min_client','num_round','algo')

admin.site.register(FlResults,FlResultsAdmin)