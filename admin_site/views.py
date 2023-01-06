from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db.models import Sum, Q,F
from django.core.mail import send_mail

from datetime import datetime
from landing_page.forms import SignUpForm
import random



from django.contrib.auth.decorators import login_required, permission_required



# Create your views here.
@login_required(login_url='landing_page:login')
def dashboard_admin(request):
    transaction_OnlineSales = Transaction.objects.all().aggregate(data =Sum('transaction_totalprice'))['data']
    transaction_pos_payment = Pos_Payment.objects.filter(pos_status = 'Printed').aggregate(data =Sum('pos_TotalAmount'))['data']
    transaction_count = Transaction.objects.count()
    transaction_pending = Transaction.objects.filter(transaction_orderstatus = "Pending").count()
    transaction_completed = Transaction.objects.filter(transaction_orderstatus = "Completed").count()
    transaction_shipped = Transaction.objects.filter(transaction_orderstatus = "Out for Shipping").count()
    transaction_decline = Transaction.objects.filter(transaction_orderstatus = "Decline").count()
    context = {
        'transaction_OnlineSales': transaction_OnlineSales ,
        'transaction_pos_payment':transaction_pos_payment,
        'transaction_count': transaction_count,
        'transaction_pending':transaction_pending,
        'transaction_completed':transaction_completed,
        'transaction_shipped':transaction_shipped,
        'transaction_decline':transaction_decline

    }
    return render(request, 'admin_site/dashboard/index.html', context)

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
            messages.success(request,("sorry have an error"))
    else:
        form = SignUpForm()
    return render(request, 'admin_site/user/register.html',{'form':form})      


#list reseller
@login_required(login_url='landing_page:login')
def list_reseller(request):
    list_reseller = Reseller.objects.order_by('-id').filter(reseller_status = "active") 
    context = {'list_reseller':list_reseller}
    return render(request, 'admin_site/user/list_reseller.html', context)

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


   

   
#SETTINGS FEATURES

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
    context ={
        'list_product':list_product,
        'list_batch':list_batch
    }
    return render(request, 'admin_site/products/view_product.html', context)
    

#adding product for tbl product
@login_required(login_url='landing_page:login')
def add_product(request):
    if request.method == "POST":
        product_code = 'S4UPR'+str(random.randint(1111111,9999999))

        pcategory = request.POST['category']
        pname = request.POST['product_name']
        product_unit = request.POST['unit']
        pprice = request.POST['price']
        pstock = 0
        pstatus = "not available"
        while Product.objects.filter(product_code = product_code) is None:
            product_code = 'S4U'+str(random.randint(1111111,9999999))

        #inserting to database 
        product = Product(product_code = product_code, product_category = pcategory, product_name = pname, product_unit =product_unit, product_price = pprice, product_stock = pstock, product_status = pstatus)
        product.save()
        
        #activity log
        activity = "Adding Product"
        NewActLog = Activity_log()
        NewActLog.user_name = request.user
        NewActLog.role = request.user.role
        NewActLog.activity = activity 
        NewActLog.save()




        messages.success(request,("Successfully Product added"))
        return redirect('admin_site:add_product')
        
    return render(request, 'admin_site/products/add_product.html')    

def settings_profile(request):
    list_profile = Profile.objects.filter(list_user = request.user)
    context={
        'list_profile':list_profile
    }
    return render(request,'admin_site/profile/settings_profile.html', context)
  


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














  
       
#FOR INVENTORY FEATURES
      
#list inventory 
@login_required(login_url='landing_page:login')
def inventory(request):
    list_products = Product.objects.all().order_by('-id')
    context = {'list_products':list_products}
    return render(request, 'admin_site/inventory/add-stock.html', context)   

#updating inventory
@login_required(login_url='landing_page:login')
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

        #adding to by batch (database)
        current_product = product.product_code
        NewBatch = By_Batch()
        NewBatch.product_code = current_product 
        NewBatch.product_batch = request.POST.get('batch_no')
        NewBatch.product_quantity = request.POST.get('quantity')
        NewBatch.product_expired = request.POST.get('expdate')
        NewBatch.save()


    
        

        #activity log for adding stock
        activity = "Adding stock"
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
    list_pos = Pos.objects.filter(pos_user = current_user).order_by('-id')
    sum_amount = Pos.objects.filter(pos_user = current_user).all().aggregate(total =Sum('pos_amount'))['total']
    
  
    context = {
        'list_pos':list_pos,
        'sum_amount':sum_amount
        }
    return render(request, 'admin_site/pos/pos_admin.html', context)

def pos_receipt(request):

    pos = Pos.objects.filter(pos_user = request.user )
    pos_payment = Pos_Payment.objects.get(pos_user = request.user.role, pos_status = "not Print")
    sum_amount = Pos.objects.filter(pos_user = request.user).all().aggregate(total =Sum('pos_amount'))['total']
   
    context = {
        'list_pos':pos,
        'sum_amount':sum_amount,
        'pos_payment':pos_payment
     
    }
    return render(request, 'admin_site/pos/receipt.html', context)    

def pos_receipt_process(request):
    if request.method == "POST":
        get_paymentID = request.POST['get_id']
        pos_payment = Pos_Payment.objects.get(id = get_paymentID)
        pos_payment.pos_status = "Printed"
        pos_payment.save()

        pos = Pos.objects.filter(pos_user = request.user)
        pos.delete()
        return redirect('admin_site:pos')
        
        

def pos_addreceipt(request):
    if request.method == "POST":
       

        #saving to pos payment in databse
        pos_id = request.POST['get_id']
        if Pos_Payment.objects.filter(pos_user =request.user.role, pos_status="not Print"):
            messages.error(request,('receipt still not done'))
            return redirect('admin_site:pos')
        else:
            new_Pos_Payment = Pos_Payment()
            new_Pos_Payment.pos_user = request.user.role
            new_Pos_Payment.pos_no = pos_id
            new_Pos_Payment.pos_TotalAmount = request.POST.get('total_amount')
            new_Pos_Payment.pos_cash = request.POST.get('cash')
            
            new_Pos_Payment.pos_change = request.POST.get('change')
            new_Pos_Payment.pos_status = "not Print"
            new_Pos_Payment.save()
            return redirect('admin_site:pos_receipt')


def Click_receipt(request):
    if Pos_Payment.objects.filter(pos_user = request.user.role, pos_status = "not Print"):
        return redirect('admin_site:pos_receipt')
    else:
        return redirect('admin_site:pos')


@login_required(login_url='landing_page:login')
def minus_qty(request, productid):
    pos = Pos.objects.get(id =productid)
    current_qty = int(pos.pos_quantity)
    result = current_qty - 1
    pos.pos_quantity = result
    pos.save()

    current_amount = int(pos.pos_amount)
    current_price = int(pos.pos_price)
    result = current_amount - current_price
    pos.pos_amount = result
    pos.save()
    
    current_pcode = pos.pos_pcode
    product = Product.objects.get(product_code = current_pcode)
    current_stock = int(product.product_stock)
    retrieve_stock = current_stock + 1
    product.product_stock = retrieve_stock
    product.save()
    return redirect('admin_site:pos')

     
@login_required(login_url='landing_page:login')
def add_qty(request,productid):
    pos = Pos.objects.get(id =productid)
    current_qty = int(pos.pos_quantity)
    result = current_qty + 1
    pos.pos_quantity = result
    pos.save()

    current_amount = int(pos.pos_amount)
    current_price = int(pos.pos_price)
    result = current_amount + current_price
    pos.pos_amount = result
    pos.save()
    
    current_pcode = pos.pos_pcode
    product = Product.objects.get(product_code = current_pcode)
    current_stock = int(product.product_stock)
    minus_stock = current_stock - 1
    product.product_stock = minus_stock
    product.save()
    return redirect('admin_site:pos')


@login_required(login_url='landing_page:login')
def pos_cancel(request,productid):
    if request.method == "POST":
        cancel = Pos.objects.get(id =productid)
        current_pcode = request.POST['current_pcode']
        product = Product.objects.get(product_code = current_pcode)

        current_qty = int(request.POST['current_qty'])
        current_stock = int(product.product_stock)

        return_stock = current_stock + current_qty
        product.product_stock = return_stock
        product.save()
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
        pos_payment = Pos_Payment.objects.filter(pos_user =request.user.role, pos_status="not Print")
        pos_payment.delete()
    

        
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
        p_price = float(request.POST['product_price'])
        p_unit = request.POST['product_unit']
        p_category = request.POST['product_category']
        p_name = request.POST['product_name']
         
        # session,  getting  user name
        current_user = request.user
        
        # minus or adding to the stock
        diff = p_stock -  qty 
        amount_cart = p_price * qty
        
        #converting the data of product stock to integer
        avail_stock = int(product.product_stock)

        #checking if have already product in the cart

        status = "low stock"

        
        

        # error trapping for 0 stock    
        if Pos.objects.filter(pos_user=request.user, pos_pcode = pcode):
            messages.success(request,("you already have on the cart"))
            return redirect('admin_site:all_products')
        elif  product.product_stock == "0":
            messages.success(request,("Sorry, No Available Stock"))
            return redirect('admin_site:all_products')

        # error trapping for low stock
        elif avail_stock <  qty:
            messages.success(request,("sorry available stock not enough"))
            return redirect('admin_site:all_products')
        elif product.product_status =="n/a":
            messages.success(request,("Sorry, this Product is not Available"))
            return redirect('admin_site:all_products')       
        else:

            #updating product stock
            product.product_stock = diff
            product.save()

             #inserting product in pos table
            pos = Pos(pos_user=current_user, pos_pcode=pcode, pos_category= p_category,  pos_name = p_name, pos_unit= p_unit, pos_price = p_price, pos_quantity = qty, pos_amount = amount_cart)
            pos.save()   
            messages.info(request,("Successfully carting Products"))
            return redirect('admin_site:all_products')      
    


             
           

      
         

        










#FOR TRANSACTION FEATURES

#transaction VIEW
@login_required(login_url='landing_page:login') 
def Transaction_orders(request):
    list_transaction = Transaction.objects.filter(Q(transaction_orderstatus = "Pending")).order_by('-id')
    context = {
        'list_transaction':list_transaction
    }
    return render(request, 'admin_site/transaction/orders.html', context)

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
            'list_transaction':transaction
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

# @login_required(login_url='landing_page:login') 
# def report_sales(request):
#     list_reports = .objects.all().order_by('-id')
#     context = {
#         'list_reports':list_reports
#     }
#     return render(request, 'admin_site/reports/act_log.html', context)    
















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
           messages.success(request, ("No records found!"))
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
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/transaction/orders.html')

@login_required(login_url='landing_page:login')
def search_actlog(request):
    if request.method == "GET":
        search = request.GET.get('search')
        if search:
            list_reports = Activity_log.objects.filter(Q(user_name__icontains = search) |    Q(activity__icontains = search) | Q(role__icontains = search)).order_by('-id')
            return render(request,'admin_site/reports/act_log.html', {'list_reports':list_reports})
        else:
           messages.success(request,("No records found!"))   
           return render(request,'admin_site/reports/act_log.html')





