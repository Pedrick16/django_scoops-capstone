from django.contrib import admin
from .models import *

# Register your models here.
class ResellerAdminView(admin.ModelAdmin):
    list_display = ['reseller_fname', 'reseller_mname', 'reseller_lname', 'reseller_gender','reseller_contact','reseller_address','reseller_email','reseller_id','reseller_status']
    search_fields = ['reseller_fname','reseller_mname','reseller_lname','reseller_status']
class ProductAdminView(admin.ModelAdmin):
    list_display = ['product_code', 'product_category', 'product_name', 'product_size','product_price','product_stock','product_status','product_expiry']
    search_fields = ['product_code', 'product_category', 'product_name', 'product_size','product_price','product_stock','product_status','product_expiry']

class PosAdminView(admin.ModelAdmin):
    list_display = ['pos_user','pos_pcode', 'pos_category', 'pos_name', 'pos_size','pos_price','pos_quantity','pos_amount']
    search_fields = ['pos_pcode', 'pos_category', 'pos_name', 'pos_size','pos_price','pos_amount']



admin.site.register(Reseller, ResellerAdminView),
admin.site.register(Product, ProductAdminView),
admin.site.register(Pos, PosAdminView),