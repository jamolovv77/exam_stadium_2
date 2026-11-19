from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import *





def home(request):
    return render(request, 'home.html')




def registration(request):
    if request.method =='POST':
        data = request.POST
        if data:
            User.objects.create_user(
                username = data['username'],
                password = data['password'],
                category = data['category'],
            )
        else:
            return redirect("registration")
        return redirect("login")
    return render(request,'registration.html')

