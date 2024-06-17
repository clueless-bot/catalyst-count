from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render


def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


def signup_view(request):
    
    return render(request, "account/signup.html")


def login_view(request):
    
    return render(request, "account/login.html")


def dashboard_view(request):
    
    return render(request, "account/dashboard.html")
