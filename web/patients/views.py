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
from django.core import serializers

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
            username=req.POST.get("username")
            secret_key=req.POST.get("secret_key")
            image=req.FILES['image']
            if full_name and birth_date and phone_number and blood_type and gender and adress and description and image and username and secret_key:
                verify_patient=Patient.objects.filter(username=username)
                if verify_patient:
                    res["status"]=400
                    res["message"]="Patient username exist already please change it !"
                else:
                    Patient.objects.create(full_name=full_name,birth_date=birth_date,created_by=req.user,phone_number=phone_number,blood_type=blood_type,gender=gender,adress=adress,description=description,username=username,secret_key=secret_key,image=image)
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
                         print(files["image"])
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
    def delete(self,req,patient_id):
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            patient=Patient.objects.filter(id=patient_id).first()
            if patient :
                if patient.created_by == req.user :
                    patient.delete()
                    res["status"]=200
                    res["message"]="Patient deleted with success"
        except Exception as e:
            print(e)
        return JsonResponse(res, status = res['status'])
    
    def put(self,req,patient_id):
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            patient=Patient.objects.filter(id=patient_id).first()
            if patient :
                if patient.created_by == req.user :
                    patient.archived=True
                    patient.save()
                    res["status"]=200
                    res["message"]="Patient archived with success"
        except Exception as e:
            print(e)
        return JsonResponse(res, status = res['status'])

    def patch(self,req,patient_id):
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            patient=Patient.objects.filter(id=patient_id).first()
            if patient :
                if patient.created_by == req.user :
                    patient.archived=False
                    patient.save()
                    res["status"]=200
                    res["message"]="Patient unarchived with success"
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
        patients = Patient.objects.filter(created_by=req.user,archived=False)

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
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            xray_image=XrayImage.objects.filter(id=xray_image_id).first()
            if xray_image:
                if xray_image.patient.created_by == req.user:
                    xray_image.delete()
                    res["status"]=200
                    res["message"]="Xray image deleted with success"
            
        except Exception as e:
            print(e)
        return JsonResponse(res, status=res["status"])



class ArchiveView(View):
    def get(self,req):
        archived_patients=Patient.objects.filter(created_by=req.user,archived=True)
        return render(req, 'gui/patients/patients-list-archive.html',{"archived_patients":archived_patients})
    def post(self,req):
        pass


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

class PatientLoginView(View):
    def get(self,req):
        return render(req,"gui/patients/patient-login.html")
    # img = Image.open("img_dir")
    def post(self,req):
        
        res = {"status": 500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            data=req.POST
            username=data.get("username")
            secret_key=data.get("secret_key")
            patient=Patient.objects.filter(username=username,secret_key=secret_key,archived=False).first()
            if patient:
                res["status"]=200
                res["message"]="You can check your results now !"
                res["data"]=data
                print(res["data"])

            else :
                res = {"status": 400, "message": "Please verify your information and retry !"}
        
            
        except Exception as e:
            print(e)
        return JsonResponse(res, status=res["status"],safe=False)
    
class PatientResultView(View):
    def get(self,req):
        data=req.GET
        username=data.get("username")
        secret_key=data.get("secret_key")
        patient=Patient.objects.filter(username=username,secret_key=secret_key).first()
        xray_images=XrayImage.objects.filter(patient=patient)
        context={"patient":patient,"xray_images":xray_images}
        return render(req,"gui/patients/patient-result.html",context)