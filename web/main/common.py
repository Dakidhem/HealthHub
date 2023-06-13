from validate_email import validate_email
from main.models import *
from django.contrib.auth import login

def create_user(req, res, email,username, password1, password2):
    check_username=User.objects.filter(username=username).first()
    if not check_username:
        if password1 == password2:
            if len(password1) >= 8:
                # check if email or phone number
                valid_email = validate_email(email)
                if valid_email:
                    user = User(username=username)
                    user.email = email
                    user.is_active = True
                    user.set_password(password1)
                    user.save()
                    login(req,user)
                    
                    res["status"] = 200
                    del res["message"]
                else:
                    res["message"] = "Invalid email"
            else:
                res["message"] = "The password must contain at least 8 characters"
        else:
            res["message"] = "The passwords provided are not the same"
    else:
        res["message"] = "The establishment name is already taken"