from validate_email import validate_email
from main.models import User
from django.contrib.auth import login

def create_doctor(req, res, email,username, password1, password2):
    check_username=User.objects.filter(username=username).first()
    if not check_username:
        if password1 == password2:
            if len(password1) >= 8:
                # check if email or phone number
                valid_email = validate_email(email)
                if valid_email:
                    doctor = User(username=username)
                    doctor.email = email
                    doctor.is_active = True
                    doctor.user_type="Doctor"
                    doctor.hospital=req.user
                    doctor.set_password(password1)
                    doctor.save()                    
                    res["status"] = 200
                    res["message"]="Doctor created successfully !"
                else:
                    res["message"] = "Invalid email"
            else:
                res["message"] = "The password must contain at least 8 characters"
        else:
            res["message"] = "The passwords provided are not the same"
    else:
        res["message"] = "Doctor name is already taken"