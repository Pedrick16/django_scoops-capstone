from django.contrib import admin
from .models import *

# Register your models here.
class ResellerAdminView(admin.ModelAdmin):
    list_display = ['reseller_fname', 'reseller_mname', 'reseller_lname', 'reseller_gender','reseller_contact','reseller_address','reseller_email','reseller_id','reseller_status']

admin.site.register(Reseller, ResellerAdminView),