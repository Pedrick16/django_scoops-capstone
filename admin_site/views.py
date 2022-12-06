from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db.models import Sum

from django.contrib.auth.decorators import login_required, permission_required



# Create your views here.
def dashboard_admin(request):
    return render(request, 'admin_site/dashboard/index.html')


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

# seaching
def search_product(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_products = Product.objects.filter(product_name__contains=search) 
            return render(request,'admin_site/search_bar/search_product.html', {'list_products':list_products})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/search_bar/search_product.html',{})

# seaching
def search_inventory(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_products = Product.objects.filter(product_name__contains=search) 
            return render(request,'admin_site/search_bar/search_product.html', {'list_products':list_products})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/search_bar/search_product.html',{})
   
    
#showing to the table data 
@login_required(login_url='landing_page:login')
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
        business_permit = request.POST['Business-permit']
        #inserting to database
        reseller = Reseller(reseller_fname = f_name, reseller_mname = m_name, reseller_lname = l_name, reseller_gender = gender, reseller_contact = contact_num, reseller_address= address, reseller_email = email, reseller_id = valid_id, reseller_businessp =business_permit, reseller_status=status)
        reseller.save()
        messages.info(request,"Successfully")
    else:
        pass    
    return render(request, 'landing_page/inquiry_reseller.html')

#adding reseller to table 
def add_reseller(request):
    if request.method =="POST":

        #activity log function
        current_user = request.user
        activity = "Adding Reseller"
        status= "active"
        
        #coming from input fields
        f_name = request.POST['fname']
        m_name = request.POST['mname']
        l_name = request.POST['lname']
        gender = request.POST['gender']
        contact_num= request.POST['cnum']
        address = request.POST['address']
        email = request.POST['email']
        valid_id = request.POST['valid-ID']
        business_permit = request.POST['Business-permit']


        #finding if email already exist
        if Reseller.objects.filter(reseller_email =  email):
            messages.success(request,("Email already exist"))
            return redirect('admin_site:add_reseller')
        else:
            #if none then saving to the database
            reseller = Reseller(reseller_fname = f_name, reseller_mname = m_name, reseller_lname = l_name, reseller_gender = gender, reseller_contact = contact_num, reseller_address= address, reseller_email = email, reseller_id = valid_id, reseller_businessp =business_permit, reseller_status=status)
            reseller.save()

            #saving to activity log
            activity_log = Activity_log(user_name = current_user, activity = activity)
            activity_log.save()

            #showing message
            messages.info(request,"Successfully")
            return redirect('admin_site:add_reseller')
    else:
        pass

    return render(request, 'admin_site/user/add_reseller.html')

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

        #activity log for adding stock
        current_user = request.user
        activity = "Adding Stock"

        #the  stock and quantity from input
        product_stock = int(request.POST['stock'])
        product_qty = int(request.POST['quantity'])
        
        #the sum of quantity and stock
        sum = product_stock + product_qty

        #update product stock
        product.product_stock = sum 
        product.save()
        activity_log = Activity_log(user_name = current_user, activity = activity)
        activity_log.save()
        messages.info(request,("Successfully Updated"))
    return redirect('admin_site:inventory')  

def pos(request):
    current_user = request.user
    list_pos = Pos.objects.order_by('-id').filter(pos_user = current_user)
    sum_amount = Pos.objects.filter(pos_user = current_user).all().aggregate(data =Sum('pos_amount'))
    
    context = {
        'list_pos':list_pos,
        'sum_amount':sum_amount
        }
    return render(request, 'admin_site/pos/pos_admin.html', context)

def pos_cancel(request,productid):
    cancel = Pos.objects.get(id =productid)
    cancel.delete()
    messages.success(request,("Successfully cancelled"))
    return redirect('admin_site:pos')


def pos_compute(request):
    if request.method == "POST":
        current_user = request.user
        cash = int(request.POST['cash'])
        sum_amount = Pos.objects.filter(pos_user = current_user).all().aggregate(data =Sum('pos_amount'))    
        total_amount = int(sum_amount)   
        if cash > total_amount:
            c =  total_amount - cash
            messages.success(request,("Successfully"))
            return redirect('admin_site:pos')
        else:
            messages.success(request,("Invalid Payment"))
            return redirect('admin_site:pos')
    else:
        context={
            'c':c
        }
        return render(request,'admin_site/pos/pos_admin.html',context)
      
# def pos_compute(request):
#     if request.method == "POST":
#         total_amount = int(request.POST['total'])
#         cash = int(request.POST['cash'])

           
#         if cash < total_amount:
#              messages.success(request,("Invalid Payment"))
#         else:
#             c = total_amount - cash
#             render(request,' admin_site/pos/pos_admin.html', {'c':c})      
         
#     return render(request,' admin_site/pos/pos_admin.html', {'c':c})        

#all products for pos
def all_products(request):
    list_products = Product.objects.order_by('-id')
    context = {'list_products':list_products}
    return render(request, 'admin_site/pos/all-products.html', context)

def cart_products(request, productid):
    if request.method =="POST":
        # getting id 
        product = Product.objects.get(id = productid)

        # coming from  input type
        qty = int(request.POST['quantity'])
        p_stock = int(request.POST['stock'])
        pcode = request.POST['product_code']
        p_price = int(request.POST['product_price'])
        p_size = request.POST['product_size']
        p_category = request.POST['product_category']
        p_name = request.POST['product_name']
         
        # session,  getting  user name
        current_user = request.user
        
        # minus or adding to the stock
        diff = p_stock -  qty 
        amount_cart = p_price * qty
        
        #converting the data of product stock to integer
        avail_stock = int(product.product_stock)

         # error trapping for 0 stock    
        if  product.product_stock == "0":
            messages.success(request,("Sorry, No Available Stock"))
            return redirect('admin_site:all_products')

        # error trapping for low stock
        elif avail_stock <  qty:
            messages.success(request,("sorry available stock not enough"))
            return redirect('admin_site:all_products')
        else:

            #updating product stock
            product.product_stock = diff
            product.save()

             #inserting product in pos table
            pos = Pos(pos_user=current_user, pos_pcode=pcode, pos_category= p_category,  pos_name = p_name, pos_size= p_size, pos_price = p_price, pos_quantity = qty, pos_amount = amount_cart)
            pos.save()
            messages.info(request,("Successfully carting Products"))
            return redirect('admin_site:all_products')


# def register(request):
#     return render(request,'admin_site/user/register_user.html')

