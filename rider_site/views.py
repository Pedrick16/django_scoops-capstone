from django.shortcuts import render, redirect
from admin_site.models import *
from datetime import datetime
from django.contrib import messages

# Create your views here.
def dashboard(request):
    return render(request, 'rider_site/dashboard/index.html')

def deliver_orders(request):
    status = "Out for Shipping"
    list_transaction = Transaction.objects.filter(transaction_orderstatus = status)
    context = {
        'list_transaction': list_transaction
    }
    return render(request, 'rider_site/deliver_orders/deliver_orders.html', context)

def orders_completed(request, orderid):
    if request.method == "POST":
        transaction = Transaction.objects.get(id = orderid)
        now = datetime.now()
        status = "Completed"
        transaction.transaction_delivered = now
        transaction.transaction_orderstatus = status
        transaction.save()
        messages.success(request, ("Successfully Delivered"))
        return redirect('rider_site:orders_completed')





