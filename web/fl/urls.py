from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required


app_name = 'fl'

urlpatterns = [
    path('', login_required(FlHome.as_view()), name="fl"),
    
]
