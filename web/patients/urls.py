from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required


app_name = 'patients'

urlpatterns = [
    path('add-patient/', login_required(AddPatient.as_view()), name="add-patient"),
    path('<int:patient_id>/edit-patient/', login_required(EditPatient.as_view()), name="edit-patient"),
    path('my-patients/', login_required(MyPatient.as_view()), name="my-patients"),
    path('xray-image/<int:patient_id>/add-xray-image', login_required(AddXrayImageView.as_view()), name='add-xray-image'),
    path('xray-image/edit-xray-image/<int:xray_image_id>', login_required(EditXrayImageView.as_view()), name='edit-xray-image'),
    path('my-patient/archive/',login_required(ArchiveView.as_view()),name="archive"),
    path('makePrediction/', login_required(MakePrediction.as_view()), name='delete-xray-image'),
]
