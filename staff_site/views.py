from django.shortcuts import render
from admin_site.models import *
from django.db.models import Sum



# Create your views here.
def dashboard(request):
    transaction_pending = Transaction.objects.filter(transaction_orderstatus = "Pending").count()
    transaction_pos_payment = Cart_Payment.objects.filter(cart_status = 'Printed').aggregate(data =Sum('cart_TotalAmount'))['data']
    context = {
        'transaction_pos_payment':transaction_pos_payment,
        'transaction_pending':transaction_pending
    }
    return render(request, 'staff_site/dashboard/index.html', context)


