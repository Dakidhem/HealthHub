from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from . models import *
from django.db.models import Q
from django.urls import reverse
from PIL import Image
from django.views.decorators.csrf import csrf_exempt
from django.http import  JsonResponse
import json, requests
from django.conf import settings
from io import BytesIO
# Create your views here.




def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    xray_images=XrayImage.objects.filter(patient=patient)
    return render(request, 'patients/patient-detail.html', {
        'patient':patient,
        'xray_images':xray_images
    })




class AddPatient(View):
    def get(self,req):
        return render(req, 'gui/patients/add-patient.html')
    
    def post(self, req):
        res = {"status":500, "message": "There was an error please verify the data provided and retry"}
        try:
            print(req.POST)
            full_name=req.POST.get("full_name")
            birth_date=req.POST.get("birth_date")
            phone_number=req.POST.get("phone_number")
            blood_type=req.POST.get("blood_type")
            gender=req.POST.get("gender")
            adress=req.POST.get("adress")
            description=req.POST.get("description")
            image=req.FILES['image']
            if full_name and birth_date and phone_number and blood_type and gender and adress and description and image:
                Patient.objects.create(full_name=full_name,birth_date=birth_date,created_by=req.user,phone_number=phone_number,blood_type=blood_type,gender=gender,adress=adress,description=description,image=image)
                res["status"]=200
                res["message"]="Patient created with success"
            else :
                res["status"]=400
                res["message"]="Please retry and verify if there is a missing field or incorrect data"
            
        except Exception as e:
            print(e)
            

        return JsonResponse(res, status=res["status"])


class EditPatient(View):
    def get(self,req,patient_id):
        patient=Patient.objects.filter(id=patient_id).first()
        xray_images=XrayImage.objects.filter(patient=patient)
        return render(req, 'gui/patients/edit-patient.html', {'patient':patient,"xray_images":xray_images
    })
    def post(self,req,patient_id):
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            files = req.FILES
            body = req.POST
            data={}
            for key in body:
                data[key] = body[key]
            patient = Patient.objects.filter(id=patient_id).first()
            if patient :
                if patient.created_by == req.user :
                    for attr, value in data.items(): 
                            setattr(patient, attr, value)
                    if files:
                         patient.image=files["image"]
                    patient.save() 
                    res['status'] = 200
                    res['message'] = "Patient updated with success"
                else :
                    res['status'] = 401
                    res['message'] = "Unauthorized"

        except Exception as e:
            print(e)
        return JsonResponse(res, status = res['status'])



@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
    patient.delete()
    return redirect('patients:my-patients')

@login_required
def my_patients(request):
    patients = Patient.objects.filter(created_by=request.user)
    return render(request, 'patients/patients-list.html', {
        'patients': patients,
        'title': 'My patients',
    })

class MyPatient(View):
    def get(self,req):
        patients = Patient.objects.filter(created_by=req.user)

        return render(req, 'gui/patients/patients-list.html', {
            'patients': patients,
        })
    
class AddXrayImageView(View):
    def get(self,req,patient_id):
        print(patient_id)
        patient=Patient.objects.filter(id=patient_id).first()
        if patient:
            return render(req,"gui/xray/add-xray-image.html",{"patient":patient})
        else :
            return redirect("home")  
        
    def post(self,req,patient_id):
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            files = req.FILES
            data = req.POST
            patient=Patient.objects.filter(id=patient_id).first()
            type=data.get("type")
            diagnostic=data.get("diagnostic")
            print(type,diagnostic)
            if patient and type and diagnostic and files :
                xray_image=XrayImage.objects.create(patient=patient,diagnostic=data.get("diagnostic"),xray_image=files["image"],type=data.get("type"))
                res["status"]=200
                res["message"]="Xray image added with success"
            else :
                res["status"]=400
                res["message"]="Please provide all the necessary data !"

            
        except Exception as e:
            print(e)
        return JsonResponse(res, status=res["status"])


class EditXrayImageView(View):
    def get(self,req,xray_image_id):
        xray_image=XrayImage.objects.filter(id=xray_image_id).first()
        return render(req,"gui/xray/edit-xray-image.html",{'xray_image':xray_image})
    
    def post(self,req,xray_image_id):
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            files = req.FILES
            data = req.POST
            xray_image=XrayImage.objects.filter(id=xray_image_id).first()

            if data.get("type"):
                xray_image.type=data.get("type")

            if data.get("diagnostic"):
                xray_image.diagnostic=data.get("diagnostic")

            if files:
                xray_image.xray_image=files['image']

            xray_image.save()

            res["status"]=200
            res["message"]="Xray image modified with success"
        except Exception as e:
            print(e)
        return JsonResponse(res, status=res["status"])
    
    def delete(self,req,xray_image_id):
        pass

@login_required
def search_patients(request):
    search_query = request.GET.get('search_query')
    patients = Patient.objects.filter(full_name__icontains=search_query, created_by=request.user)
    context = {
        'title': 'My patients',
        'patients': patients
    }
    return render(request, 'patients/patients-list.html', context)



@login_required
def add_xray_image(request, patient_id):
    patient=get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST' and request.FILES['upload']:
        xray_image=XrayImage.objects.create(patient=patient,xray_image=request.FILES['upload'])
        return redirect('patients:patient-detail', patient_id=patient.id)

    return render(request, 'patients/add-xray-image.html')



@login_required
def edit_xray_image(request, xray_image_id):
    xray_image=get_object_or_404(XrayImage, id=xray_image_id)
    return render(request, 'patients/edit-xray-image.html',{'xray_image':xray_image})


@login_required
def delete_xray_image(request, xray_image_id):
    xray_image = get_object_or_404(XrayImage, id=xray_image_id)
    xray_image.delete()
    return redirect('patients:patient-detail', patient_id=xray_image.patient.id)


class MakePrediction(View):
    # img = Image.open("img_dir")
    def post(self,req):
        
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            files=req.FILES
            data = req.POST
            print(data)
            image_url = data.get("image_url")
            print(image_url)
            image=None
            if files:
                image=req.FILES['image']
            elif image_url:
                image = open("/app"+image_url, 'rb')
        
            files = {'file': image}
            getdata = requests.post("http://host.docker.internal:7000/predict", files=files)
            res["status"]=200
            res["data"]=getdata.json()

        
            
        except Exception as e:
            print(e)
        return JsonResponse(res, status=res["status"])
