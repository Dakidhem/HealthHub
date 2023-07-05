from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

app_name = 'hospital'


urlpatterns = [
    path('list-doctors/', login_required(ListOfDoctors.as_view()), name="list-doctors"),
    path('add-doctor/', login_required(AddDoctor.as_view()), name="add-doctor"),
    path('edit-doctor/<int:doctor_id>/', login_required(EditDoctor.as_view()), name="edit-doctor"),
    
]
