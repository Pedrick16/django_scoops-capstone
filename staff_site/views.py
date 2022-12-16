from django.shortcuts import render
from admin_site.models import *



# Create your views here.
def dashboard(request):
    transaction_pending = Transaction.objects.filter(transaction_orderstatus = "Pending").count()
    context = {
        'transaction_pending':transaction_pending,
    }
    return render(request, 'staff_site/dashboard/index.html', context)


