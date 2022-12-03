from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db.models import Q

from django.contrib.auth.decorators import login_required, permission_required



# Create your views here.
@login_required(login_url='landing_page:login')
#list reseller
def list_reseller(request):
    list_reseller = Reseller.objects.order_by('-id').filter(reseller_status = "active") 
    context = {'list_reseller':list_reseller}
    return render(request, 'admin_site/user/list_reseller.html', context)

#archiving reseller
def archive_reseller(request,resellerid):
    reseller = Reseller.objects.get(id = resellerid)
    reseller.delete()
    messages.success(request,("Successfully Archiving Reseller info"))
    return redirect('admin_site:list_reseller')


# def search(request):
#     return render(request,'admin_site/search_bar/search_reseller.html')
def search_reseller(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_reseller = Reseller.objects.filter(reseller_fname__contains=search, reseller_status ="active") 
            return render(request,'admin_site/search_bar/search_reseller.html', {'list_reseller':list_reseller})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/search_bar/search_reseller.html',{})


def search_product(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_products = Product.objects.filter(product_name__contains=search) 
            return render(request,'admin_site/search_bar/search_product.html', {'list_products':list_products})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/search_bar/search_product.html',{})

def search_inventory(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_products = Product.objects.filter(product_name__contains=search) 
            return render(request,'admin_site/search_bar/search_product.html', {'list_products':list_products})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/search_bar/search_product.html',{})
   
    

@login_required(login_url='landing_page:login')
#list inventory 
def list_inquiry(request):
    list_inquiry = Reseller.objects.order_by('-id').filter(reseller_status = "pending")
    context = {'list_inquiry':list_inquiry}
    return render(request, 'admin_site/user/list_inquiry.html', context)

#process inquiry for reseller
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

#list inventory 
def list_products(request):
    list_products = Product.objects.order_by('-id')
    context = {'list_products':list_products}
    return render(request, 'admin_site/products/product.html', context)

#list inventory 
def inventory(request):
    list_products = Product.objects.order_by('-id')
    context = {'list_products':list_products}
    return render(request, 'admin_site/inventory/add-stock.html', context)   

#updating inventory
def update_inventory(request, productid):
    if request.method == "POST":
        #to get the latest id
        product = Product.objects.get(id = productid)

        #the  stock and quantity from input
        product_stock = int(request.POST['stock'])
        product_qty = int(request.POST['quantity'])
        
        #the sum of quantity and stock
        sum = product_stock + product_qty

        #update product stock
        product.product_stock = sum 
        product.save()
        messages.info(request,("Successfully Updated"))
    return redirect('admin_site:inventory')  

def pos(request):
    list_pos = Pos.objects.order_by('-id')
    context = {'list_pos':list_pos}
    return render(request, 'admin_site/pos/pos_admin.html', context)

#all products for pos
def all_products(request):
    list_products = Product.objects.order_by('-id')
    context = {'list_products':list_products}
    return render(request, 'admin_site/pos/all-products.html', context)  

# def register(request):
#     return render(request,'admin_site/user/register_user.html')

