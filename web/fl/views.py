from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from .models import *

class FlHome(View):
    def get(self,req):
        return render(req,"fl/fl-main.html")