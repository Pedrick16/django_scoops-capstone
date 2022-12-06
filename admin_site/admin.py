from django.contrib import admin
from .models import *

# Register your models here.
class ResellerView(admin.ModelAdmin):
    list_display = ['reseller_fname', 'reseller_mname', 'reseller_lname', 'reseller_gender','reseller_contact','reseller_address','reseller_email','reseller_id','reseller_businessp','reseller_status']
    search_fields = ['reseller_fname','reseller_mname','reseller_lname','reseller_status']
class ProductView(admin.ModelAdmin):
    list_display = ['product_code', 'product_category', 'product_name', 'product_size','product_price','product_stock','product_status','product_expiry']
    search_fields = ['product_code', 'product_category', 'product_name', 'product_size','product_price','product_stock','product_status','product_expiry']

class PosView(admin.ModelAdmin):
    list_display = ['pos_user','pos_pcode', 'pos_category', 'pos_name', 'pos_size','pos_price','pos_quantity','pos_amount']
    search_fields = ['pos_pcode', 'pos_category', 'pos_name', 'pos_size','pos_price','pos_amount']

class Activity_logView(admin.ModelAdmin):
    list_display = ['user_name','activity','date_time']
    search_fields = ['user_name','activity','date_time']






admin.site.register(Reseller, ResellerView),
admin.site.register(Product, ProductView),
admin.site.register(Pos, PosView),
admin.site.register(Activity_log, Activity_logView),