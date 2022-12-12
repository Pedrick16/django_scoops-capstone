from django.shortcuts import render


# Create your views here.
def dashboard(request):
    return render(request, 'staff_site/dashboard/index.html')

