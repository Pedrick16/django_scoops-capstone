from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
@login_required(login_url='landing_page:login')
def list_reseller(request):
    list_reseller = Reseller.objects.order_by('-id').filter(reseller_status = "active") 
    context = {'list_reseller':list_reseller}
    return render(request, 'admin_site/user/list_reseller.html', context)

@login_required(login_url='landing_page:login')
def list_inquiry(request):
    list_inquiry = Reseller.objects.order_by('-id').filter(reseller_status = "pending")
    context = {'list_inquiry':list_inquiry}
    return render(request, 'admin_site/user/list_inquiry.html', context)


def process_inquiry(request):
    if request.method =="POST":
        status= "pending"
        f_name = request.POST['fname']
        m_name = request.POST['mname']
        l_name = request.POST['lname']
        gender = request.POST['gender']
        contact_num= request.POST['cnum']
        address = request.POST['address']
        email = request.POST['email']
        valid_id = request.POST['valid-ID']
        #inserting to database
        reseller = Reseller(reseller_fname = f_name, reseller_mname = m_name, reseller_lname = l_name, reseller_gender = gender, reseller_contact = contact_num, reseller_address= address, reseller_email = email, reseller_id = valid_id, reseller_status=status)
        reseller.save()
        messages.info(request,"Successfully")
    else:
        pass    
    return render(request, 'landing_page/inquiry_reseller.html')    
