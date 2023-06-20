from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from main.models import User
from .common import *

class AddDoctor(View):
    def get(self,req):
        if req.user.user_type == "Hospital":
            return render(req,"gui/hospital/add-doctor.html")
        else :
            return redirect("home")
    def post(self,req):
        res = {"status":500, "message": "Une erreur est survenue, veuillez réessayer."}
        #username,email,password,confirm_password
        try:
            data=req.POST
            email=data.get("email")
            username=data.get("username")
            password1=data.get("password1")
            password2=data.get("password2")

            if email and username and password1 and password2:
                user = User.objects.filter(email=email)
                if user:
                    res["message"] = "A doctor with this email exist already"
                else:
                    create_doctor(req,res, email,username, password1, password2)
        except Exception as e:
            print(e)
            

        return JsonResponse(res, status=res["status"])

class ListOfDoctors(View):
    def get(self,req):
        if req.user.user_type == "Hospital":
            doctors=User.objects.filter(hospital=req.user,user_type="Doctor")
            return render(req,"gui/hospital/list-doctors.html",{"doctors":doctors})
        else :
                return redirect("home")

class EditDoctor(View):
    def get(self,req,doctor_id):
        if req.user.user_type == "Hospital":
            doctor=User.objects.filter(id=doctor_id)
            return render(req,"gui/hospital/list-doctors.html",{"doctor":doctor})
        else :
            return redirect("home")
        
    def post(self,req,doctor_id):
        res = {"status":500, "message": "Une erreur est survenue, veuillez réessayer."}
        doctor=User.objects.filter(id=doctor_id)
        try:
            pass

        except Exception as e:
            print(e)
            

        return JsonResponse(res, status=res["status"])
    
    def delete(self,req,doctor_id):
        res = {"status":500, "message": "Une erreur est survenue, veuillez réessayer."}
        
        try:
            doctor=User.objects.filter(id=doctor_id).first()
            if doctor:
                doctor.delete()
                res["status"]=200
                res["message"]="Doctor deleted with success"
            else :
                res["status"]=200
                res["message"]="This docotr doesnt exist"
        except Exception as e:
            print(e)
            

        return JsonResponse(res, status=res["status"])