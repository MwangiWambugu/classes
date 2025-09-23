from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.contrib import auth
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django .urls import reverse
from .utils import token_generator

# Create your views here.


class emailValidationView(View):
    def post(self, request):
        data= json.loads(request.body)
        email= data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': "email is invalid"}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': "Sorry email in Use"}, status=400)
        
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data= json.loads(request.body)
        username= data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': "username should only contain alphanumeric characters"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': "Sorry Username in Use"}, status=400)
        
        return JsonResponse({'username_valid': True})
    # def post(self, request):
    #     return render(request, "authentication/register.html")


class registrationView(View):
    def get(self, request):
        return render(request, "authentication/register.html")
    
    def post(self, request):
        # get user data
        # validate
        # create a user account
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")

        # check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "authentication/register.html")

        # check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "authentication/register.html")

        # check password length
        if len(password) < 6:
            messages.error(request, "Password too short (min 6 chars)")
            return render(request, "authentication/register.html")

        # if everything is fine → create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False # for email verification   
        user.save()
        email_subject = "Activate your account"
        
        # path_to_view
        # getting domains
        # relative url for verification
        # token
        domain=get_current_site(request).domain
        link = reverse('activate', kwargs={
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user)
        })
        
        email_body = "Hi " + user.username + \
            " Please use this link to verify your account \n" + \
            "http://" + domain + link
        email = EmailMessage(
        email_subject,
        email_body,
        "noreply@semicolon.com",
        [email],
        
    )
        email.send(fail_silently=False)

        messages.success(request, "Account created successfully! Please log in.")
        return render(request, "authentication/register.html")


class verificationView(View):
    def get(self, request, uidb64, token):
        # return render(request, "authentication/verification.html")
        return redirect("login")
    