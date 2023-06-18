from django.urls import path, include
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('signin/', SignInView.as_view(), name="signin"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signout/', signout, name='signout'),
    path('flatpages/', include('django.contrib.flatpages.urls')),
    path('profile/', login_required(Profile.as_view()), name='profile'),
    path('edit-profile/', edit_user, name='edit_profile'),
    path('change-password/', change_password, name='change-password'),
    path('user-profile/<int:pk>/delete-account/', DeleteUserView.as_view(),name='delete-account'),
    path('contact-us/',ContactView.as_view(),name="contact-us"),
    path('privacy/',TemplateView.as_view(template_name="gui/others/privacy.html"),name="privacy"),
    path('terms/',TemplateView.as_view(template_name="gui/others/terms.html"),name="terms"),
    path('about/',TemplateView.as_view(template_name="gui/others/about.html"),name="about"),
]
