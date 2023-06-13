from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from .models import *
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import DeleteView
import json
from django.http import JsonResponse
from .common import *


class HomeView(TemplateView):
    template_name = "gui/home/home.html"

class SignInView(View):
    def get(self,req):
        if req.user.is_authenticated:
            return redirect("home")
        return render(req,'gui/account/signin.html')

    def post(self, req):
        res = {"status":500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            data = json.loads(req.body)
            email = data.get('email')
            password = data.get('password')
            username=User.objects.filter(email=email).first()
            user = authenticate(req, username = username, password = password)
            if user:
                login(req, user)
                res['success'] = True
                res['status'] = 200
                res['message'] = 'Logged in'
            else:
                res['status'] = 401
                res['message'] = 'Invalid email or password'
        except Exception as e:
            print(e)
        return JsonResponse(res, status=res["status"])



class SignUpView(View):

    def get(self, req):
        if req.user.is_authenticated:
            return redirect("home")
        return render(req, "gui/account/signup.html")

    def post(self, req):
        res = {"status":500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            data = json.loads(req.body)
            email = data.get("email")
            username = data.get("username")
            password1 = data.get("password1")
            password2 = data.get("password2")
            if email and username and password1 and password2:
                user = User.objects.filter(email=email)
                if user:
                    res["message"] = "Un utilisateur avec cet email existe déjà."
                else:
                    create_user(req,res, email,username, password1, password2)

                    
        except Exception as e:
            print(e)
            

        return JsonResponse(res, status=res["status"])



def signout(request):
    logout(request)
    return redirect('/')


def user_profile(request):
    user = get_object_or_404(User, id=request.user.id)

    return render(request,'main/user-profile.html', {
        'user': user,
    })

class Profile(View):
    def get(self, req):
        return render(req, "gui/account/profile.html")



@login_required
def edit_user(request):
    pass



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'main/change_password.html', {'form': form})


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('signout')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.success(request, "Your account has been deleted.")
        logout(request)
        self.object.delete()
        return redirect(success_url)


class ContactView(View):

    def get(self, req):

        return render(req, "gui/others/contact.html")

    def post(self, req):
        res = {"status":500, "message": "Une erreur est survenue, veuillez réessayer."}
        try:
            data=req.POST
            email=data.get("email")
            subject=data.get("subject")
            message=data.get("message")  
            if email and subject and message:
                if req.user.is_authenticated:
                    contact_message=ContactMessage.objects.create(email=email,subject=subject,message=message,user=req.user)
                else :
                    contact_message=ContactMessage.objects.create(email=email,subject=subject,message=message)
            
                res['status'] = 200
                res['message'] = 'Message sent successfully'
            else:
                res['status'] = 400
                res['message'] = 'Please verify the data provided'

        except Exception as e:
            print(e)
            

        return JsonResponse(res, status=res["status"])