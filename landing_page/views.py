from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from .models import *
from admin_site.models import *
from .forms import RegisterForm






# Create your views here.

# first landing of page
def landing_page(request):
    return render(request, 'landing_page/index.html')


# login process for multi user
def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user =  authenticate(request,username=username, password=password)
        activity = "signed-in"
    
        if user is not None:
            # current_user =  User.objects.get(pk=user.pk)
            login(request, user)  
            activity_log = Activity_log(user_name = username, activity = activity)
            activity_log.save()

            if user.role == "admin": 
                return redirect('admin_site:dashboard') 
            elif user.role == "reseller":
                return redirect('reseller_site:dashboard')
            elif user.role == "rider":    
                return redirect('rider_site:dashboard')
            elif user.role == "staff": 
                return redirect('staff_site:dashboard')
            else: 
                messages.success(request, ("There was an error logging in, Try Again ..."))
                return redirect('landing_page:login') 

           
        else:
            messages.success(request, ("There was an error logging in, Try Again ..."))
            return redirect('landing_page:login') 
    
    return render(request, 'landing_page/login-folder/login.html')


@login_required(login_url='landing_page:login')
def registerUser(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_site:list_reseller')
    return render(request, 'admin_site/user/register_user.html',{'form':form})     


       





# def loginView(request):
#     # current_user =  User.objects.get(pk=user.pk)
#     if request.method == 'POST':
#         username= request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
   
#         if user is not None and user.role == "admin":
#             login(request, user)
#             return redirect('landing_page:dashboard_admin')
#         elif user is not None and user.role == "reseller":
#             login(request, user)
#             return redirect('landing_page:dashboard_staff') 
#         elif user is not None and user.role == "staff":
#             login(request, user)
#             return redirect('landing_page:dashboard_staff')
#         elif user is not None and user.role == "rider":
#             login(request, user)
#             return redirect('scoops_admin:list_reseller')  
#         else:
#             messages.success(request, ("There Was An Error Logging In, Try Again ..."))
#             return render(request,'landing_page/login-folder/login.html') 
#     else:
#         return render(request, 'landing_page/login-folder/login.html')    

# logout session here.
@login_required(login_url='landing_page:login')
def logoutView(request):
    current_user = request.user
    activity = "signed-out"
    logout(request)
    activity_log = Activity_log(user_name =current_user, activity = activity)
    activity_log.save()
    return render(request, 'landing_page/login-folder/login.html')

# for inquiry here.

def inquiry_reseller(request):
    return render(request, 'landing_page/inquiry_reseller.html')    


# dashboard for admin_site.



# dashboard for staff_site.


 

    