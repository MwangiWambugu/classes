from .views import registrationView
from django.urls import path
from .views import UsernameValidationView,emailValidationView,verificationView, loginView, logoutView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path("register/", registrationView.as_view(), name="register"),
    path("login/", loginView.as_view(), name="login"),
    path("validate_username/",csrf_exempt(UsernameValidationView.as_view()), name="validate_username"),
    path("validate_email/",csrf_exempt(emailValidationView.as_view()), name="validate_email"),
    path("activate/<uidb64>/<token>/", verificationView.as_view(), name="activate"),
    path("logout/", logoutView.as_view(), name="logout"),
]
