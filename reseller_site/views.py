from django.shortcuts import render, redirect
from admin_site.models import *
from django.db.models import Sum

# Create your views here.
def landing(request):
    return render(request, 'reseller_site/landing.html')

def orders_reseller(request):
    return render(request, 'reseller_site/orders/order.html')

def checkout(request):
    list_cart = Pos.objects.filter(pos_user = request.user).order_by('-id')
    sum_amount = Pos.objects.filter(pos_user = request.user).all().aggregate(data =Sum('pos_amount'))
    context = {
        'list_cart':list_cart,
        'sum_amount':sum_amount
    }
    return render(request, 'reseller_site/cart/checkout.html', context)

def cart_reseller(request):
    if request.method == "POST":
        current_user = request.user
        pos = Pos.objects.get(list_user = current_user )
     

        fullname = request.POST['fullname']
        address = request.POST['address']
        contact_no = request.POST['contact_no']
        delivery_option = request.POST['delivery_option']
        pos_pcategory = pos.pos_category
        pos_pname = pos.pos_name
        pos_pcategory = pos.pos_size
        pos_pcategory = pos.pos_quantity
        pos_pcategory = pos.pos_amount

    



        fullname = request.POST['fullname']
        address = request.POST['address']
        contact_no = request.POST['contact_no']
        delivery_option = request.POST['delivery_option']
        pos_pcategory = pos.pos_category
        pos_pname = pos.pos_name
        pos_pcategory = pos.pos_size
        pos_pcategory = pos.pos_quantity
        pos_pcategory = pos.pos_amount

        transaction = Transaction

        

    

       
