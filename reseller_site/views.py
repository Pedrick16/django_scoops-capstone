from django.shortcuts import render, redirect
from admin_site.models import *
from django.db.models import Sum
from django.contrib import messages

# Create your views here.
def landing(request):
    return render(request, 'reseller_site/landing.html')

def orders_reseller(request):
    return render(request, 'reseller_site/orders/order.html')

def cart_reseller(request):
    list_cart = Pos.objects.filter(pos_user = request.user).order_by('-id')
    sum_amount = Pos.objects.filter(pos_user = request.user).all().aggregate(data =Sum('pos_amount'))
    context = {
        'list_cart':list_cart,
        'sum_amount':sum_amount
    }
    return render(request, 'reseller_site/cart/checkout.html', context)

def checkout(request):
    if request.method == "POST":
        current_user = request.user
        pos = Pos.objects.filter(pos_user = current_user )

        fullname = request.POST['fullname']
        address = request.POST['address']
        contact_no = request.POST['contact_no']
        delivery_option = request.POST['option']

        total_amount = float(request.POST['total_amount'])

        status = "Pending"

        transaction = Transaction(transaction_user = current_user, transaction_fullname = fullname, transaction_address = address, transaction_contactno = contact_no, transaction_doption =delivery_option,  transaction_totalprice = total_amount, transaction_orderstatus = status)
        transaction.save()
        pos.delete()
        messages.success(request, ("Please wait your order"))
        return redirect('admin_site:pos')
  
       



 
      

        

    

       
