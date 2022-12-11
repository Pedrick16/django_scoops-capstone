from django.shortcuts import render, redirect
from admin_site.models import *
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='landing_page:login')
def landing(request):
    return render(request, 'reseller_site/landing.html')

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

        fname = request.POST['fname']
        lname = request.POST['lname']
        address = request.POST['address']
        contact_no = request.POST['contact_no']
        delivery_option = request.POST['option']

        total_amount = float(request.POST['total_amount'])

        status = "Pending"

        transaction = Transaction(transaction_user = current_user, transaction_fname = fname,transaction_lname = lname, transaction_address = address, transaction_contactno = contact_no, transaction_doption =delivery_option,  transaction_totalprice = total_amount, transaction_orderstatus = status)
        transaction.save()
        
        NewOrderItems = Pos.objects.filter(pos_user = request.user)
        for item in NewOrderItems:
            OrderItem.objects.create(
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
  

      

       



 
      

        

    

       
