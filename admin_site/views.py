from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db.models import Sum, Q,F, Max
from django.core.mail import send_mail

from datetime import datetime,date
from landing_page.forms import SignUpForm,ChangePasswordForm
from landing_page.models import User

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import random, locale
from decimal import Decimal
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
@login_required(login_url='landing_page:login')
def dashboard_admin(request):
    

    now = datetime.now()
    transaction_OnlineSales = Transaction.objects.filter(created_at = now).aggregate(data =Sum('transaction_totalprice'))['data']
    transaction_pos_payment = Cart_Payment.objects.filter(cart_status = 'Printed', cart_date=now).aggregate(data =Sum('cart_TotalAmount'))['data']
    transaction_count = Transaction.objects.count()
    transaction_pending = Transaction.objects.filter(transaction_orderstatus = "Pending").count()
    transaction_completed = Transaction.objects.filter(transaction_orderstatus = "Completed").count()
    transaction_shipped = Transaction.objects.filter(transaction_orderstatus = "Out for Shipping").count()
    transaction_decline = Transaction.objects.filter(transaction_orderstatus = "Decline").count()
    
    context = {
        'transaction_OnlineSales': transaction_OnlineSales,
        'transaction_pos_payment':transaction_pos_payment,
        'transaction_count': transaction_count,
        'transaction_pending':transaction_pending,
        'transaction_completed':transaction_completed,
        'transaction_shipped':transaction_shipped,
        'transaction_decline':transaction_decline
    }
    return render(request, 'admin_site/dashboard/index.html', context)



def add_useraccount(request):
    if request.method =="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_site:send_email')
    else:
        form = SignUpForm()
    return render(request, 'admin_site/user/add_useraccount.html',{'form':form})

# def change_password(request):
#     if request.method == 'POST':
#         form = ChangePasswordForm(request.POST)
#         if form.is_valid():
#             user = request.user
#             current_password = form.cleaned_data['current_password']
#             new_password = form.cleaned_data['new_password']
#             if user.check_password(current_password):
#                 user.set_password(new_password)
#                 user.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('admin_site:change_password')
#             else:
#                 form.add_error('current_password', 'Incorrect password')
#     else:
#         form = ChangePasswordForm()
#     return render(request, 'admin_site/user/changepass.html', {'form': form})     


def register(request, inquiryid):
    if request.method =="POST":
        reseller = Reseller.objects.get(id = inquiryid)
        status = "active"
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #changing status for reseller
            reseller.reseller_status = status  
            reseller.save()
            return redirect('admin_site:send_email')
    else:
        form = SignUpForm()
    return render(request, 'admin_site/user/register.html',{'form':form})      



#list reseller
@login_required(login_url='landing_page:login')
def list_reseller(request):
    list_reseller = Reseller.objects.order_by('-id').filter(reseller_status = "active") 
    context = {'list_reseller':list_reseller}
    return render(request, 'admin_site/user/list_reseller.html', context)

#list user account
@login_required(login_url='landing_page:login')
def user_list(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'admin_site/user/useraccount.html', context)


#list user account
@login_required(login_url='landing_page:login')
def edit_user_account(request,userid):
    list_users = User.objects.get(id = userid)
    context={
        'list_users':list_users
    }
    return render(request, 'admin_site/edit/edit_useraccount.html',context)

@login_required(login_url='landing_page:login')
def update_user_account(request,userid):
    if request.method == "POST":
        user = User.objects.get(id = userid)
        username =  request.POST['username']
        email = request.POST['email']
        role =  request.POST['role']
        status = request.POST['status']
        user.username = username
        user.email=    email
        user.role =  role
        user.status = status
        user.save()
        messages.success(request,"successfully updated")
        return redirect('admin_site:user_list')


#showing to the table data 
@login_required(login_url='landing_page:login')
def list_inquiry(request):
    list_inquiry = Reseller.objects.order_by('-id').filter(reseller_status = "pending")
    context = {'list_inquiry':list_inquiry}
    return render(request, 'admin_site/user/list_inquiry.html', context)



#adding reseller to table 
@login_required(login_url='landing_page:login')
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
            #activity log for adding stock
            activity = "Adding Reseller"
            NewActLog = Activity_log()
            NewActLog.user_name = request.user
            NewActLog.role = request.user.role
            NewActLog.activity = activity 
            NewActLog.save()
    

            #showing message
            messages.info(request,"Successfully")
            return redirect('admin_site:add_reseller')
    else:
        pass

    return render(request, 'admin_site/user/add_reseller.html')

def view_pic(request,id):
    reseller = Reseller.objects.get(id =id)
    context={
        'reseller':reseller
    }
    return render(request,'admin_site/user/view_pic.html',context)    


def edit_reseller(request,id):
    list_reseller = Reseller.objects.get(id = id)
    context={
        'list_reseller':list_reseller,
    }
    return render(request,'admin_site/edit/edit_reseller.html',context)   

def update_reseller(request,id ):
    if request.method == "POST":
        reseller = Reseller.objects.get(pk=id)
        reseller.reseller_fname = request.POST.get('fname')
        reseller.reseller_mname = request.POST.get('mname')
        reseller.reseller_lname = request.POST.get('lname')
        reseller.reseller_gender = request.POST.get('gender')
        reseller.reseller_contact = request.POST.get('cnumber')
        reseller.reseller_address = request.POST.get('address')
        reseller.reseller_email = request.POST.get('email')
        reseller.save()
        messages.success(request,("Successfully Updated"))
        return redirect('admin_site:list_reseller')
   

    




#archiving reseller
@login_required(login_url='landing_page:login')
def archive_reseller(request,resellerid):
    if request.method =="POST":
        # changing status to inactice
        reseller = Reseller.objects.get(id = resellerid)
        # reseller.delete()
        status = "inactive"
        reseller.reseller_status = status
        reseller.save()
        
        #activity log for archiving reseller
        activity = "archiving reseller"
        NewActLog = Activity_log()
        NewActLog.user_name = request.user
        NewActLog.role = request.user.role
        NewActLog.activity = activity 
        NewActLog.save()
    

        messages.success(request,("Successfully Archiving Reseller info"))
        return redirect('admin_site:list_reseller')






@login_required(login_url='landing_page:login')
def send_email(request):
    if request.method == "POST":
     
        tile_email = "your inquiry successfully approved"
        # tile_email = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(
            tile_email,
            message,
            'settings.EMAIL_HOST_USER',
            [email],
            fail_silently=False)
        return redirect('admin_site:list_reseller')

    return render(request, 'admin_site/user/send_email.html')        



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
        valid_id = request.FILES.get('valid-ID')
        business_permit = request.FILES.get('business_permit')
        #inserting to database
        if Reseller.objects.filter(reseller_email = email):
            messages.success(request,("Email already Exist"))
            return redirect('landing_page:inquiry_reseller')
        else:
            reseller = Reseller(reseller_fname = f_name, reseller_mname = m_name, reseller_lname = l_name, reseller_gender = gender, reseller_contact = contact_num, reseller_address= address, reseller_email = email, reseller_id = valid_id, reseller_businessp =business_permit, reseller_status=status)
            reseller.save()
            messages.success(request,("Successfully Submitted"))
    return render(request, 'landing_page/inquiry_reseller.html')







#FOR PRODUCT FEATURES
#list product
@login_required(login_url='landing_page:login')
def list_products(request):
    list_products = Product.objects.all().order_by('-id')
    context = {'list_products':list_products}
    return render(request, 'admin_site/products/product.html', context)

#viewing product
@login_required(login_url='landing_page:login')
def view_product(request, productid):
    list_product = Product.objects.get(id = productid)
    current_pcode = list_product.product_code
    list_batch = By_Batch.objects.filter(product_code = current_pcode)
    latest_bnumber = By_Batch.objects.filter(product_code = current_pcode).aggregate(max = Max('product_batch'))['max']
    context ={
        'list_product':list_product,
        'list_batch':list_batch,
        'latest_bnumber': latest_bnumber
    }
    return render(request, 'admin_site/products/view_product.html', context)

def add_product(request):
        list_settings = Settings.objects.all()
        context={
            'list_settings':list_settings
        }
        return render(request, 'admin_site/products/add_product.html',context)


#adding product for tbl product
@login_required(login_url='landing_page:login')
def process_product(request):
    if request.method == "POST":

        product_code = 'S4UPR'+str(random.randint(1111111,9999999))

        pcategory = request.POST['category']
        pname = request.POST['product_name']
        product_unit = request.POST['unit']
        r_price = int(request.POST['reseller_price'])
        pprice = int(request.POST['price'])
        pstock = 0
        pstatus = "not available"

        # locale.setlocale(locale.LC_ALL, 'en_PH.UTF-8')
        # decimal_sales = Decimal(r_price)
        # reseller_price = locale.currency(decimal_sales, grouping=True, symbol=True)

        # locale.setlocale(locale.LC_ALL, 'en_PH.UTF-8')
        # decimal_sales = Decimal(pprice)
        # pos_price = locale.currency(decimal_sales, grouping=True, symbol=True)


        while Product.objects.filter(product_code = product_code) is None:
            product_code = 'S4U'+str(random.randint(1111111,9999999))

        #inserting to database 
        product = Product(product_code = product_code, product_category = pcategory, product_name = pname, product_unit =product_unit, product_ResellerPrice =r_price, product_price = pprice, product_stock = pstock, product_status = pstatus)
        product.save()
        
        #activity log
        activity = "Adding Product"
        NewActLog = Activity_log()
        NewActLog.user_name = request.user
        NewActLog.role = request.user.role
        NewActLog.activity = activity 
        NewActLog.save()


        messages.success(request,("Successfully Product added"))
        return redirect('admin_site:list_product')
   
        


def edit_product(request, productid):
    product = Product.objects.get(pk = productid)
    context = {
        'list_product':product
    }
    return render(request, 'admin_site/products/edit_product.html',context)

def update_product(request, productid):
    product = Product.objects.get(pk = productid)
    product.product_name = request.POST.get('product_name')
    product.product_category = request.POST.get('product_category')
    product.product_unit = request.POST.get('product_unit')
    product.product_ResellerPrice = request.POST.get('reseller_price')
    product.product_price = request.POST.get('pos_price')
    product.product_status = request.POST.get('status')
    product.save()
    messages.success(request, ("Successfully Updated"))
    return redirect('admin_site:list_product')
    




#settings
def settings_profile(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('admin_site:settings_profile')
            else:
                form.add_error('current_password', 'Incorrect password')
    else:
        form = ChangePasswordForm()
    
    list_profile = Profile.objects.filter(list_user = request.user)
    context={
        'list_profile':list_profile,
        'form':form
    }
    return render(request,'admin_site/profile/settings_profile.html', context)



@login_required(login_url='landing_page:login')
def list_archive(request):
    list_reseller = Reseller.objects.order_by('-id').filter(reseller_status = "inactive") 
    context = {'list_reseller':list_reseller}
    return render(request, 'admin_site/user/archive.html', context)    

@login_required(login_url='landing_page:login')
def retrieve_reseller(request,id):
    # changing status to actice
    reseller = Reseller.objects.get(id = id)
    status = "active"
    reseller.reseller_status = status
    reseller.save()
    messages.success(request,("Successfully Retrieved"))
    return redirect('admin_site:list_archive')


def add_profile(request):
    if request.method == "POST":
        
        NewProfile = Profile()
        NewProfile.list_user= request.user
        NewProfile.profile_pic = request.FILES.get('profile_pic')
        NewProfile.profile_fname = request.POST.get('first')
        NewProfile.profile_mname = request.POST.get('middle')
        NewProfile.profile_lname = request.POST.get('last')
        NewProfile.profile_cnumber = request.POST.get('contact_no')
        NewProfile.profile_address = request.POST.get('address')
        NewProfile.profile_email = request.POST.get('email')
        NewProfile.save()
        return redirect('admin_site:my_profile')

def update_profile(request,profileid):
    if request.method == "POST":
        profile = Profile.objects.get(id =profileid)

        profile_picture = request.FILES.get('profile_pic')
        profile.profile_fname = request.POST.get('first')
        profile.profile_mname = request.POST.get('middle')
        profile.profile_lname = request.POST.get('last')
        profile.profile_cnumber = request.POST.get('contact_no')
        profile.profile_address = request.POST.get('address')
        profile.profile_email = request.POST.get('email')
        if profile_picture:
            profile.profile_pic = profile_picture
        profile.save()
        return redirect('admin_site:settings_profile') 

def my_profile(request):
    current_profile = Profile.objects.filter(list_user = request.user)
    context ={
        'current_profile':current_profile
    }
    return render(request, 'admin_site/profile/my_profile.html',context)

def settings_product(request):
    settings = Settings.objects.all()
    context ={
        'settings':settings
    }
    return render(request, 'admin_site/settings/product_settings.html',context)

def settings_remove(request, id):
    settings = Settings.objects.get(pk = id)
    settings.delete()
    messages.success(request,("succussfully removed"))
    return redirect('admin_site:settings_product')


    



def settings_addproduct(request):
    if request.method == "POST":
        category = request.POST['category']
        unit = request.POST['unit']
        settings = Settings()

        if Settings.objects.filter(Q(settings_category =category) | Q(settings_unit = unit)):
            messages.error(request,("It is already Exist"))
            return redirect('admin_site:settings_product')
        else:
            settings.settings_category = request.POST.get('category')
            settings.settings_unit = request.POST.get('unit')
            settings.save()
            return redirect('admin_site:settings_product')
    return render(request, 'admin_site/settings/add_settings.html')














#FOR INVENTORY FEATURES

#list inventory 
@login_required(login_url='landing_page:login')
def inventory(request):
    list_products = Product.objects.all().order_by('-id')
    context = {'list_products':list_products}
    return render(request, 'admin_site/inventory/add-stock.html', context)   

@login_required(login_url='landing_page:login')
def view_inventory(request):
    list_inventory = By_Batch.objects.all().order_by('-id')
    context = {'list_inventory':list_inventory}
    return render(request, 'admin_site/inventory/view.html', context)  

#updating inventory
@login_required(login_url='landing_page:login')
def update_inventory(request, productid):
    if request.method == "POST":
        #to get the latest id
        product = Product.objects.get(id = productid)


        #the  stock and quantity from input
        product_stock = int(request.POST['stock'])
        product_qty = int(request.POST['quantity'])
        p_code = request.POST['product_code']
        p_batch = request.POST['batch_no']

    
        #the sum of quantity and stock
        sum = product_stock + product_qty

        if By_Batch.objects.filter(product_code = p_code, product_batch =p_batch):
            messages.info(request,("already have a batch number"))
            return redirect('admin_site:inventory') 
        else:
            #update product stock
            product.product_stock = sum 
            product.product_status = "available"
            product.save()


            #adding to by batch (database)
            current_product = product.product_code
            NewBatch = By_Batch()
            NewBatch.product_code = current_product
            NewBatch.product_name = request.POST.get('product_name')
            NewBatch.product_batch = request.POST.get('batch_no')
            NewBatch.product_quantity = request.POST.get('quantity')
            NewBatch.product_expired = request.POST.get('expdate')
            NewBatch.save()





            #activity log for adding stock
            activity = "Added stock"
            NewActLog = Activity_log()
            NewActLog.user_name = request.user
            NewActLog.role = request.user.role
            NewActLog.activity = activity 
            NewActLog.save()
            messages.info(request,("Successfully Updated"))
            return redirect('admin_site:inventory')  


















# FOR POS FEATURES

#list pos cart
@login_required(login_url='landing_page:login')
def pos(request):
    current_user = request.user
    list_pos = Cart.objects.filter(cart_user = current_user).order_by('-id')
    sum_amount = Cart.objects.filter(cart_user = current_user).all().aggregate(total =Sum('cart_amount'))['total']
    list_pospayment = Cart_Payment.objects.filter(cart_status = "not Print")
    


    context = {
        'list_pos':list_pos,
        'sum_amount':sum_amount,
        'list_pospayment':list_pospayment

        }
    return render(request, 'admin_site/pos/pos_admin.html', context)

def pos_receipt(request):

    pos = Cart.objects.filter(cart_user = request.user )
    pos_payment = Cart_Payment.objects.get(cart_user = request.user.role, cart_status = "not Print")
    sum_amount = Cart.objects.filter(cart_user = request.user).all().aggregate(total =Sum('cart_amount'))['total']

    
    context = {
        'list_pos':pos,
        'sum_amount':sum_amount,
        'pos_payment':pos_payment
    }
    return render(request, 'admin_site/pos/receipt.html', context)    


def pos_receipt_process(request):
    if request.method == "POST":
        get_paymentID = request.POST['get_id']
        pos = Cart.objects.filter(cart_user = request.user)
        if Cart.objects.filter(cart_user = request.user):

            for carts in pos:

                products = Product.objects.get(product_code = carts.cart_pcode)
                cart_quantity = int(carts.cart_quantity)
                current_stock = int(products.product_stock)
                minus_stock = cart_quantity - current_stock
                products.product_stock = minus_stock
                products.save()
            
                if products.product_stock == 0:
                    products.product_status = "not available"
                    products.save()

           
            pos_payment = Cart_Payment.objects.get(id = get_paymentID)
            pos_payment.cart_status = "Printed"
            pos_payment.save()

            pos = Cart.objects.filter(cart_user = request.user)
            pos.delete()
            return redirect('admin_site:pos')

def pos_addreceipt(request):
    if request.method == "POST":

        #saving to pos payment in databse
        pos_id = request.POST['get_id']

        pos = Cart.objects.filter(cart_user = request.user)

        for carts in pos:
                    


            products = Product.objects.get(product_code = carts.cart_pcode)
                   
            
            if products.product_stock < carts.cart_quantity:
                 
                messages.error(request,('Some Products out of stock'))
                return redirect('admin_site:pos')
                
            
        


        if Cart_Payment.objects.filter(cart_user =request.user.role, cart_status="not Print"):
            messages.error(request,('receipt still not done'))
            return redirect('admin_site:pos')
        else:
            new_Cart_Payment = Cart_Payment()
            new_Cart_Payment.cart_user = request.user.role
            new_Cart_Payment.cart_no = pos_id
            new_Cart_Payment.cart_TotalAmount = request.POST.get('total_amount')
            new_Cart_Payment.cart_cash = request.POST.get('cash')
            
            new_Cart_Payment.cart_change = request.POST.get('change')
            new_Cart_Payment.cart_status = "not Print"
            new_Cart_Payment.save()
            return redirect('admin_site:pos_receipt')

def pos_removeall(request):
    pos = Cart.objects.filter(cart_user = request.user)
    pos.delete()
    messages.success(request,("successfully removed all"))
    return redirect('admin_site:pos')


def Click_receipt(request):
    if Cart_Payment.objects.filter(cart_user = request.user.role, cart_status = "not Print"):
        return redirect('admin_site:pos_receipt')
    else:
        return redirect('admin_site:pos')


@login_required(login_url='landing_page:login')
def minus_qty(request, productid):
    pos = Cart.objects.get(id =productid)
    if pos.cart_quantity == 1:
        pos.delete()
        return redirect('admin_site:pos')
    else:
        current_qty = int(pos.cart_quantity)
        result = current_qty - 1
        pos.cart_quantity = result
        pos.save()

        current_amount = int(pos.cart_amount)
        current_price = int(pos.cart_price)
        result = current_amount - current_price
        pos.cart_amount = result
        pos.save()
    
        # current_pcode = pos.cart_pcode
        # product = Product.objects.get(product_code = current_pcode)
        # current_stock = int(product.product_stock)
        # retrieve_stock = current_stock + 1
        # product.product_stock = retrieve_stock
        # product.save()

        # if product.product_stock > 0:
        #         product.product_status = "available"
        #         product.save()
        return redirect('admin_site:pos')

     
@login_required(login_url='landing_page:login')
def add_qty(request,productid):
    pos = Cart.objects.get(id =productid)
    current_qty = int(pos.cart_quantity)
    result = current_qty + 1

    #for checking product code
    current_pcode = pos.cart_pcode

    product = Product.objects.get(product_code = current_pcode)
    if product.product_stock == 0:
        messages.success(request,("No available Stock"))
        return redirect('admin_site:pos')
    else:
        pos.cart_quantity = result
        pos.save()

        current_amount = int(pos.cart_amount)
        current_price = int(pos.cart_price)
        result = current_amount + current_price
        pos.cart_amount = result
        pos.save()
    

        # product = Product.objects.get(product_code = current_pcode)
        # current_stock = int(product.product_stock)
        # minus_stock = current_stock - 1
        # product.product_stock = minus_stock
        # product.save()

        # if product.product_stock == 0:
        #     product.product_status = "not available"
        #     product.save()

        return redirect('admin_site:pos')


@login_required(login_url='landing_page:login')
def pos_cancel(request,productid):
    if request.method == "POST":
        cancel = Cart.objects.get(id =productid)
        current_pcode = request.POST['current_pcode']
        # product = Product.objects.get(product_code = current_pcode)

        # current_qty = int(request.POST['current_qty'])
        # current_stock = int(product.product_stock)

        # return_stock = current_stock + current_qty
        # product.product_stock = return_stock
        

        # product.save()
        cancel.delete()

        #activity log for cancelling the product
        activity = "Cancelled Cart"
        NewActLog = Activity_log()
        NewActLog.user_name = request.user
        NewActLog.role = request.user.role
        NewActLog.activity = activity 
        NewActLog.save()

        #removing in pos payment
        # pos_id = request.POST['pos_id']
        pos_payment = Cart_Payment.objects.filter(cart_user =request.user.role, cart_status="not Print")
        pos_payment.delete()

        # if product.product_stock != 0:
        #         product.product_status = "available"
        #         product.save()
    

        
        messages.success(request,("Successfully cancelled"))
        return redirect('admin_site:pos')

    
      
#all products for pos
@login_required(login_url='landing_page:login')
def all_products(request):
    list_products = Product.objects.all()
    context = {'list_products':list_products}
    return render(request, 'admin_site/pos/all-products.html', context)


#adding to pos cart
@login_required(login_url='landing_page:login')
def cart_products(request, productid):
    if request.method =="POST":
        # getting id 
       
        product = Product.objects.get(id = productid)
        
       

        # coming from  input type
        qty = int(request.POST['quantity'])
        p_stock = int(request.POST['stock'])
        pcode = request.POST['product_code']
        p_reseller_price = int(request.POST['product_reseller_price'])
        p_price = int(request.POST['product_price'])
        p_unit = request.POST['product_unit']
        p_category = request.POST['product_category']
        p_name = request.POST['product_name']

       
         
        # session,  getting  user name
        current_user = request.user
        
        # minus or adding to the stock
        # diff = p_stock -  qty 
        amount_cart = p_price * qty
        reseller_cart = p_reseller_price * qty
        
        #converting the data of product stock to integer
        avail_stock = int(product.product_stock)

        #checking if have already product in the cart

        status = "low stock"

        
        

        # error trapping for 0 stock    
        if Cart.objects.filter(cart_user=request.user, cart_pcode = pcode):
            messages.error(request,("you already have on the cart"))
            return redirect('admin_site:all_products')
        elif  product.product_stock == 0:
            messages.error(request,("Sorry, No Available Stock"))
            return redirect('admin_site:all_products')

        # error trapping for low stock
        elif avail_stock <  qty:
            messages.error(request,("sorry available stock not enough"))
            return redirect('admin_site:all_products')
        elif product.product_status =="not available":
            messages.error(request,("Sorry, this Product is not Available"))
            return redirect('admin_site:all_products')       
        else:

            #updating product stcart
            # product.product_stock = diff
            # product.save()

            #inserting product in pos table
            pos = Cart(cart_user=current_user, cart_pcode=pcode, cart_category= p_category,  cart_name = p_name, cart_unit= p_unit,cart_reseller_price =p_reseller_price , cart_price = p_price, cart_quantity = qty, cart_amount = amount_cart,  cart_ResellerAmount =reseller_cart )
            pos.save()   

            pos_payment = Cart_Payment.objects.filter(cart_user = request.user, cart_status="not Print")
            pos_payment.delete()

            # if product.product_stock == 0:
            #     product.product_status = "not available"
            #     product.save()
            


        
            messages.success(request,("Successfully carting Products"))
            return redirect('admin_site:pos')      
    













#FOR TRANSACTION FEATURES

#transaction VIEW
@login_required(login_url='landing_page:login') 
def Transaction_orders(request):
    list_transaction = Transaction.objects.filter(Q(transaction_orderstatus = "Pending")).order_by('-id')
    transaction_pending = Transaction.objects.filter(transaction_orderstatus = "Pending").count()
    context = {
        'list_transaction':list_transaction,
        'transaction_pending':transaction_pending
    }
    return render(request, 'admin_site/transaction/orders.html', context)


@login_required(login_url='landing_page:login') 
def Transaction_outshipping(request):
    list_transaction = Transaction.objects.filter(Q(transaction_orderstatus = "Out for Shipping")).order_by('-id')
    context = {
        'list_transaction':list_transaction
    }
    return render(request, 'admin_site/transaction/orders.html', context)



@login_required(login_url='landing_page:login') 
def Transaction_completed(request):
    list_transaction = Transaction.objects.filter(Q(transaction_orderstatus = "Completed")).order_by('-id')
    context = {
        'list_transaction':list_transaction
    }
    return render(request, 'admin_site/transaction/orders.html', context)



@login_required(login_url='landing_page:login')
def delivery_process(request):
    if request.method == "POST":
        transaction_no = request.POST['transaction_no']
        transaction = Transaction.objects.get(transaction_no = transaction_no)
        transaction.transaction_orderstatus = "Out for Shipping"
        transaction.save()
        messages.success(request,("Out for Shipping"))
        return redirect('admin_site:transaction_outshipping')





@login_required(login_url='landing_page:login')
def completed_process(request):
    if request.method == "POST":
        transaction_no = request.POST['transaction_no']
        transaction = Transaction.objects.get(transaction_no = transaction_no)
        transaction.transaction_orderstatus = "Completed"
        transaction.save()
        messages.success(request,("Successfully Delivered"))
        return redirect('admin_site:transaction_completed')







@login_required(login_url='landing_page:login') 
def transaction_view(request, id):
    if request.method == "GET":
        transaction = Transaction.objects.get(id = id)

        transaction_no = transaction.transaction_no
        list_orderitem = OrderItem.objects.filter(OrderItem_transactionNo = transaction_no).order_by('-id')

        list_total = OrderItem.objects.filter(OrderItem_transactionNo = transaction_no).all().aggregate(data=Sum('OrderItem_amount'))
        context = {
            'list_orderitem':list_orderitem,
            'list_total':list_total,
            'list_transaction':transaction,
        }
    return render(request, 'admin_site/transaction/view_orders.html', context)




#FOR REPORTS FEATURES
#reports VIEW
@login_required(login_url='landing_page:login') 
def report_actlog(request):
    list_reports = Activity_log.objects.all().order_by('-id')
    context = {
        'list_reports':list_reports
    }
    return render(request, 'admin_site/reports/act_log.html', context)



@login_required(login_url='landing_page:login') 
def report_pos_sales(request):
    pos_payment = Cart_Payment.objects.filter(cart_status = 'Printed')
    context = {
        'pos_payment':pos_payment
    }
    return render(request, 'admin_site/reports/pos_sales.html',context)




@login_required(login_url='landing_page:login') 
def report_online_sales(request):
    transaction = Transaction.objects.filter(transaction_orderstatus = 'Completed')
    context = {
        'transaction':transaction
    }
    return render(request, 'admin_site/reports/online_sales.html',context) 










#SEARCH FEATURES

#search bar for reseller
@login_required(login_url='landing_page:login')
def search_reseller(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_reseller = Reseller.objects.filter(Q(reseller_status = "active"), Q(reseller_fname__contains=search) | Q(reseller_mname__contains=search) |Q(reseller_lname__contains=search) | Q(reseller_gender__contains=search) | Q(reseller_address__contains=search)| Q(reseller_email__contains=search)) 
            return render(request,'admin_site/user/list_reseller.html', {'list_reseller': list_reseller})
        else:
           messages.error(request,("No records found!"))   
           return render(request,'admin_site/user/list_reseller.html')

#search bar for reseller
@login_required(login_url='landing_page:login')
def search_archive(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_reseller = Reseller.objects.filter(Q(reseller_status = "inactive"), Q(reseller_fname__contains=search) | Q(reseller_mname__contains=search) |Q(reseller_lname__contains=search) | Q(reseller_gender__contains=search) | Q(reseller_address__contains=search)| Q(reseller_email__contains=search)) 
            return render(request,'admin_site/user/archive.html', {'list_reseller': list_reseller})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/user/list_reseller.html')

#search bar for inventory
@login_required(login_url='landing_page:login')
def search_inventory(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_products = Product.objects.filter(Q(product_code__icontains = search) | Q(product_name__icontains = search)) 
            return render(request,'admin_site/inventory/add-stock.html', {'list_products':list_products})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/inventory/add-stock.html')

    
#search bar for Products             


@login_required(login_url='landing_page:login')
def search_product(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_products = Product.objects.filter(Q(product_code__icontains=search) | Q(product_category__icontains=search) | Q(
                product_name__icontains=search) | Q(product_unit__icontains=search) | Q(product_stock__icontains=search) | Q(product_status__icontains=search))
            return render(request, 'admin_site/products/product.html', {'list_products': list_products})
        else:
           messages.error(request, ("No records found!"))
           return render(request, 'admin_site/products/product.html')


#search bar for Products             
@login_required(login_url='landing_page:login')
def search_transaction(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_transaction= Transaction.objects.filter(Q(transaction_orderstatus = "Pending"),    Q(transaction_no__icontains = search) | Q(transaction_fname__icontains = search) ) 
            return render(request,'admin_site/transaction/orders.html', {'list_transaction':list_transaction})
        else:
           messages.error(request,("No records found!"))   
           return render(request,'admin_site/transaction/orders.html')

@login_required(login_url='landing_page:login')
def search_actlog(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_reports = Activity_log.objects.filter(Q(user_name__icontains = search) |    Q(activity__icontains = search) | Q(role__icontains = search)).order_by('-id')
            return render(request,'admin_site/reports/act_log.html', {'list_reports':list_reports})
        else:
           messages.error(request,("No records found!"))   
           return render(request,'admin_site/reports/act_log.html')


@login_required(login_url='landing_page:login')
def search_date_actlog(request):
    if request.method == "POST":
        start_date= request.POST['start_date']
        end_date = request.POST['end_date']

        list_reports = Activity_log.objects.filter(date_time__date__range=[start_date, end_date])

        context ={
            'list_reports':list_reports
        }
        return render(request,'admin_site/reports/act_log.html',context)
    return render(request,'admin_site/reports/act_log.html')



@login_required(login_url='landing_page:login')
def search_online_sales(request):
    if request.method == "POST":
        start_date= request.POST['start_date']
        end_date = request.POST['end_date']
        transaction = Transaction.objects.filter(created_at__range=[start_date,end_date])
        list_transaction = Transaction.objects.filter(created_at__range=[start_date,end_date]).aggregate(total=Sum('transaction_totalprice'))['total']
        context = {
            'transaction':transaction,
            'list_transaction':list_transaction
        }
        return render(request, 'admin_site/reports/online_sales.html',context)
    return render(request, 'admin_site/reports/online_sales.html')

@login_required(login_url='landing_page:login')
def search_pos_sales(request):
    if request.method == "POST":
        start_date= request.POST['start_date']
        end_date = request.POST['end_date']
        pos_payment = Cart_Payment.objects.filter(cart_date__range=[start_date,end_date])
        list_pos_payment = Cart_Payment.objects.filter(cart_status = 'Printed', cart_date__range=[start_date,end_date]).aggregate(total=Sum('cart_TotalAmount'))['total']

        context = {
            'pos_payment':pos_payment,
            'list_transaction':list_pos_payment
        }
        return render(request, 'admin_site/reports/pos_sales.html',context)
    return render(request, 'admin_site/reports/pos_sales.html')
    


    







