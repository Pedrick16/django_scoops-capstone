from django.shortcuts import render, redirect
from admin_site.models import *
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random

# Create your views here.
@login_required(login_url='landing_page:login')
def dashboard(request):
    return render(request, 'reseller_site/dashboard/index.html')

@login_required(login_url='landing_page:login')
def orders_reseller(request):
    list_transaction = Transaction.objects.filter(transaction_user = request.user).order_by('-id')
    context = {
        'list_transaction':list_transaction
    }
    return render(request, 'reseller_site/orders/orders.html',context)

@login_required(login_url='landing_page:login')
def cart_reseller(request):
    list_cart = Pos.objects.filter(pos_user = request.user).order_by('-id')
    sum_amount = Pos.objects.filter(pos_user = request.user).all().aggregate(data =Sum('pos_amount'))
    context = {
        'list_cart':list_cart,
        'sum_amount':sum_amount
    }
    return render(request, 'reseller_site/cart/checkout.html', context)

@login_required(login_url='landing_page:login')
def checkout(request):
    if request.method == "POST":
        current_user = request.user
        pos = Pos.objects.filter(pos_user = current_user )

        status = "Pending"
        trackno = 'S4U'+str(random.randint(1111111,9999999))

        NewTransaction = Transaction()
        NewTransaction.transaction_user = request.user
        NewTransaction.transaction_fname = request.POST.get('fname')
        NewTransaction.transaction_lname = request.POST.get('lname')
        NewTransaction.transaction_address = request.POST.get('address')
        NewTransaction.transaction_contactno= request.POST.get('contact_no')
        NewTransaction.transaction_doption = request.POST.get('option')
        NewTransaction.transaction_totalprice = float(request.POST.get('total_amount'))
        NewTransaction.transaction_orderstatus = status

        while Transaction.objects.filter(transaction_no = trackno) is None:
            trackno = 'S4U'+str(random.randint(1111111,9999999))

        NewTransaction.transaction_no = trackno   
        NewTransaction.save()

       
        
        NewOrderItems = Pos.objects.filter(pos_user = request.user)
        for item in NewOrderItems:
            OrderItem.objects.create(
                OrderItem_transactionNo = trackno,
                OrderItem_user = item.pos_user,
                OrderItem_category = item.pos_category,
                OrderItem_name = item.pos_name,
                OrderItem_size = item.pos_size,
                OrderItem_quantity  = item.pos_quantity,
                OrderItem_amount= item.pos_amount
            )
            pos.delete()
    messages.success(request, ("Please wait for your order"))
    return redirect('admin_site:pos')




  

      

       



 
      

        

    

       
