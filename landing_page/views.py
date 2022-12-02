from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *

# Create your views here.

# first landing of page
def landing_page(request):
    return render(request, 'landing_page/index.html')


# login process for multi user
def loginView(request):
    # current_user =  User.objects.get(pk=user.pk)
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
   
        if user is not None and user.role == "admin":
            login(request, user)
            return redirect('landing_page:dashboard_admin')
        elif user is not None and user.role == "reseller":
            login(request, user)
            return redirect('scoops_admin:list_reseller') 
        elif user is not None and user.role == "staff":
            login(request, user)
            return redirect('scoops_admin:list_reseller')
        elif user is not None and user.role == "rider":
            login(request, user)
            return redirect('scoops_admin:list_reseller')  
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again ..."))
            return render(request,'landing_page/login-folder/login.html') 
    else:
        return render(request, 'landing_page/login-folder/login.html')    

# logout session here.
def logoutView(request):
    logout(request)
    return render(request, 'landing_page/login-folder/login.html')

# for inquiry here.
def inquiry_reseller(request):
    return render(request, 'landing_page/inquiry_reseller.html')    

# dashboard for admin_site.
def dashboard_admin(request):
    return render(request, 'admin_site/dashboard/index.html')