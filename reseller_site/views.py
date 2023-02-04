from django.shortcuts import render, redirect
from admin_site.models import *
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random



# Create your views here.
@login_required(login_url='landing_page:login')
def dashboard(request):
    list_numberorder =    Transaction.objects.filter(transaction_user = request.user).count()
    transaction_pending = Transaction.objects.filter(transaction_user = request.user,transaction_orderstatus = "Pending").count()
    transaction_shipped = Transaction.objects.filter(transaction_user = request.user,transaction_orderstatus = "Out for Delivery").count()
    transaction_decline = Transaction.objects.filter(transaction_user = request.user,transaction_orderstatus = "Decline").count()
    context={
        'list_numberorder':list_numberorder,
        'transaction_pending':transaction_pending,
        'transaction_shipped':transaction_shipped,
        'transaction_decline':transaction_decline
    }
    return render(request, 'reseller_site/dashboard/index.html',context)

# @login_required(login_url='landing_page:login')
# def orders_reseller(request):
#     list_transaction = Transaction.objects.filter(transaction_user = request.user).order_by('-id')
#     context = {
#         'list_transaction':list_transaction
#     }
#     return render(request, 'reseller_site/orders/orders.html',context)

@login_required(login_url='landing_page:login')
def cart_reseller(request):
    total_item = Pos.objects.filter(pos_user = request.user).count()
    list_cart = Pos.objects.filter(pos_user = request.user).order_by('-id')
    sum_amount = Pos.objects.filter(pos_user = request.user).all().aggregate(data =Sum('pos_ResellerAmount'))
    context = {
        'list_cart':list_cart,
        'sum_amount':sum_amount,
        'total_item':total_item
    }
    return render(request, 'reseller_site/cart/checkout.html', context)

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

    #for checking product code
    current_pcode = pos.pos_pcode

    product = Product.objects.get(product_code = current_pcode)
    if product.product_stock == 0:
        messages.success(request,("No available Stock"))
        return redirect('admin_site:pos')
    else:
        pos.pos_quantity = result
        pos.save()

        current_amount = int(pos.pos_amount)
        current_price = int(pos.pos_price)
        result = current_amount + current_price
        pos.pos_amount = result
        pos.save()
    

        product = Product.objects.get(product_code = current_pcode)
        current_stock = int(product.product_stock)
        minus_stock = current_stock - 1
        product.product_stock = minus_stock
        product.save()
        return redirect('admin_site:pos')

@login_required(login_url='landing_page:login')
def checkout(request):
    if request.method == "POST":
        current_user = request.user
        pos = Pos.objects.filter(pos_user = current_user)
        preferred_date = request.POST['prefer_date']
        no_specific = "None"
        status = "Pending"
        trackno = 'S4U'+str(random.randint(1111111, 9999999))
        if preferred_date:
            NewTransaction = Transaction()
            NewTransaction.transaction_user = request.user
            NewTransaction.transaction_fname = request.POST.get('fname')
            NewTransaction.transaction_lname = request.POST.get('lname')
            NewTransaction.transaction_address = request.POST.get('address')
            NewTransaction.transaction_contactno= request.POST.get('contact_no')
            NewTransaction.transaction_doption = request.POST.get('option')
            NewTransaction.transaction_preferred_date = preferred_date 
            NewTransaction.transaction_totalprice = float(request.POST.get('total_amount'))
            NewTransaction.transaction_orderstatus = status


        
            while Transaction.objects.filter(transaction_no = trackno) is None:
                trackno = 'S4U'+str(random.randint(1111111,9999999))

            NewTransaction.transaction_no = trackno   
            NewTransaction.save()

            #activity log for Checkout
            activity = "Check-out"
            NewActLog = Activity_log()
            NewActLog.user_name = request.user
            NewActLog.role = request.user.role
            NewActLog.activity = activity 
            NewActLog.save()
        

            NewOrderItems = Pos.objects.filter(pos_user = request.user)
            for item in NewOrderItems:
                OrderItem.objects.create(
                    OrderItem_transactionNo = trackno,
                    OrderItem_category = item.pos_category,
                    OrderItem_name = item.pos_name,
                    OrderItem_unit = item.pos_unit,
                    OrderItem_quantity  = item.pos_quantity,
                    OrderItem_amount= item.pos_amount
                )
                pos.delete()
            messages.success(request, ("Please wait for your order"))
            return redirect('reseller_site:transaction_orders')
        else:
            NewTransaction = Transaction()
            NewTransaction.transaction_user = request.user
            NewTransaction.transaction_fname = request.POST.get('fname')
            NewTransaction.transaction_lname = request.POST.get('lname')
            NewTransaction.transaction_address = request.POST.get('address')
            NewTransaction.transaction_contactno= request.POST.get('contact_no')
            NewTransaction.transaction_doption = request.POST.get('option')
            NewTransaction.transaction_preferred_date = no_specific
            NewTransaction.transaction_totalprice = float(request.POST.get('total_amount'))
            NewTransaction.transaction_orderstatus = status

        
            while Transaction.objects.filter(transaction_no = trackno) is None:
                trackno = 'S4U'+str(random.randint(1111111,9999999))

            NewTransaction.transaction_no = trackno   
            NewTransaction.save()


            #activity log for Checkout
            activity = "Check-out"
            NewActLog = Activity_log()
            NewActLog.user_name = request.user
            NewActLog.role = request.user.role
            NewActLog.activity = activity 
            NewActLog.save()
        

            NewOrderItems = Pos.objects.filter(pos_user = request.user)
            for item in NewOrderItems:
                OrderItem.objects.create(
                    OrderItem_transactionNo = trackno,
                    OrderItem_category = item.pos_category,
                    OrderItem_name = item.pos_name,
                    OrderItem_unit = item.pos_unit,
                    OrderItem_quantity  = item.pos_quantity,
                    OrderItem_amount= item.pos_amount
                )
                pos.delete()
            messages.success(request, ("Please wait for your order"))
            return redirect('reseller_site:transaction_orders')


@login_required(login_url='landing_page:login') 
def transaction_orders(request):
    list_transaction = Transaction.objects.filter(transaction_user= request.user).order_by('-id')
    context = {
        'list_transaction':list_transaction
    }
    return render(request, 'reseller_site/orders/orders.html', context)


#list reseller cart
@login_required(login_url='landing_page:login')
def add_cart(request):
    current_user = request.user
    list_pos = Pos.objects.filter(pos_user = current_user).order_by('-id')
    sum_amount = Pos.objects.filter(pos_user = current_user).all().aggregate(total =Sum('pos_ResellerAmount'))['total']
    

    context = {
        'list_pos':list_pos,
        'sum_amount':sum_amount
        }
    return render(request, 'reseller_site/cart/cart.html', context)


@login_required(login_url='landing_page:login') 
def transaction_view(request,id):

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
    
    return render(request, 'reseller_site/orders/view_orders.html', context)




@login_required(login_url='landing_page:login')
def cart_cancel(request,productid):
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



