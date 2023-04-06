from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required


from django.contrib import messages
from .models import *
from admin_site.models import *








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

            #activity log for login
            activity = "Signed-in"
            NewActLog = Activity_log()
            NewActLog.user_name = request.user
            NewActLog.role = request.user.role
            NewActLog.activity = activity 
            NewActLog.save()
    

            if user.role == "admin" and user.status == "active": 
                return redirect('admin_site:dashboard') 
            elif user.role == "reseller" and user.status == "active":
                return redirect('reseller_site:dashboard')
            elif user.role == "rider" and user.status == "active":    
                return redirect('rider_site:dashboard')
            elif user.role == "staff" and user.status == "active": 
                return redirect('staff_site:dashboard')
            elif user.status == "inactive": 
                messages.error(request, ("Your account is no longer active"))
                return redirect('landing_page:login') 
            else: 
                messages.error(request, ("Wrong Username and Password"))
                return redirect('landing_page:login') 

        else:
            messages.error(request, ("Wrong Username and Password"))
            return redirect('landing_page:login') 
    
    return render(request, 'landing_page/login-folder/login.html')




    
@login_required(login_url='landing_page:login')
def logoutView(request):
    
    #activity log for login
    activity = "Signed-out"
    NewActLog = Activity_log()
    NewActLog.user_name = request.user
    NewActLog.role = request.user.role
    NewActLog.activity = activity 
    NewActLog.save()

    logout(request)
    return render(request, 'landing_page/login-folder/login.html')



       





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

# for inquiry here.
def inquiry_reseller(request):
    return render(request, 'landing_page/inquiry_reseller.html')    


# dashboard for admin_site.



# dashboard for staff_site.


 

    