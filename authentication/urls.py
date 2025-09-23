from .views import registrationView
from django.urls import path
from .views import UsernameValidationView,emailValidationView,verificationView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path("register/", registrationView.as_view(), name="register"),
    path("validate-username/",csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path("validate-email/",csrf_exempt(emailValidationView.as_view()), name="validate-email"),
    path("activate/<uidb64>/<token>/", (verificationView.as_view()), name="activate"),

]
    