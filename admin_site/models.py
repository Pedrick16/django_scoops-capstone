from django.db import models
from datetime import datetime
from django.utils import timezone
import os , random




now = timezone.now()
# Create your models here.

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'image_path/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance,basename=basefilename, randomstring=randomstr, ext = file_extension, year=now.strftime('%Y'), month= _now.strftime('%m'),day=_now.strftime('$d'))





class Reseller(models.Model):

    # dropdown for status
    STATUS = (("pending","pending"),("active","active"),("inactive","inactive"))  
    BOOLCHOICE = (("Male","Male"),("Female","Female"))

    reseller_fname =models.CharField(max_length=200, verbose_name='First Name')
    reseller_mname =models.CharField(max_length=200, verbose_name='Middle Name')
    reseller_lname =models.CharField(max_length=200, verbose_name='Last Name')
    reseller_gender = models.CharField(max_length = 50,choices=BOOLCHOICE, verbose_name='Gender')
    reseller_contact =models.CharField(max_length = 12, verbose_name='Contact Number')
    reseller_address =models.TextField(null=False, verbose_name='Address')
    reseller_email =models.EmailField(unique=True, max_length=200, verbose_name='Email')
    reseller_id =models.ImageField( upload_to=image_path, verbose_name='valid id')
    reseller_businessp =models.ImageField( upload_to=image_path,verbose_name='business id')
    reseller_status =models.CharField(max_length=200, null=True, choices=STATUS, verbose_name='Status')


    def __str__(self):
        return self.reseller_email





class Product(models.Model):
    STATUS = (("available","available"),("not available","not available"))
    product_code =  models.CharField(unique=True, max_length=200, verbose_name='Product Code')
    product_category =  models.CharField(max_length=200, verbose_name='Category')
    product_name=  models.CharField(max_length=200, verbose_name='Product Name')
    product_unit =  models.CharField(max_length=200, verbose_name='Unit')
    product_ResellerPrice =   models.BigIntegerField(null=True, verbose_name='Reseller Price')
    product_price =   models.BigIntegerField(null=True, verbose_name='Pos Price')
    product_stock =  models.BigIntegerField(null=True, verbose_name='Available Stock')
    product_status =  models.CharField(max_length=200, choices=STATUS, verbose_name='Status')


    def __str__(self):
        return self.product_code


class By_Batch(models.Model):
    product_code = models.CharField( max_length=200, null=True,verbose_name='Product Code')
    product_name = models.CharField( max_length=200, null=True,verbose_name='Product Name')
    product_batch =  models.CharField(max_length=200, null=True, verbose_name='Batch Number')
    product_quantity =  models.BigIntegerField(null=True,  verbose_name='Quantity')
    product_expired =  models.DateField( null=True, verbose_name='Expiration Date')
    created_at =models.DateTimeField(default=timezone.now,  verbose_name='created')
    
    def __str__(self):
        return self.product_code

class Cart(models.Model):
    cart_user =  models.CharField(max_length=200, null=False, default=None, verbose_name='List user')
    cart_pcode =  models.CharField(max_length=200, verbose_name='Product Code')
    cart_category =  models.CharField(max_length=200, verbose_name='Category')
    cart_name=  models.CharField(max_length=200, verbose_name='Product Name')
    cart_unit =  models.CharField(max_length=200, verbose_name='Unit')
    cart_reseller_price =   models.BigIntegerField(null=True, verbose_name='Reseller Price')
    cart_price =   models.BigIntegerField(null=True, verbose_name='POS Price')
    cart_quantity =  models.BigIntegerField(null=True, verbose_name='quantity')
    cart_ResellerAmount =   models.BigIntegerField(null=True, verbose_name='Reseller Amount')
    cart_amount =  models.BigIntegerField(null=True, verbose_name='POS Amount')
    created_at =models.DateField(default=timezone.now,null=True,   verbose_name='Date Created')
    
    


    def __str__(self):
        return self.cart_user

class Cart_Payment(models.Model):
    STATUS = (("Printed","Printed"),("not Print","not Print"))
    cart_user = models.CharField(max_length=200, null=False, default=None, verbose_name='Role')
    cart_no = models.CharField(max_length=200, null=True,  verbose_name='Pos No')
    cart_TotalAmount =  models.BigIntegerField(null=True, verbose_name='Total Amount')
    cart_cash = models.BigIntegerField( null=True, verbose_name='Cash')
    cart_change =  models.DecimalField(  max_digits=12, decimal_places=2,null=True, verbose_name='Change')
    cart_status = models.CharField(max_length=250, null=True, choices=STATUS, verbose_name='Status')
    cart_date = models.DateField(default=timezone.now, verbose_name='Date')

    def __str__(self):
        return self.cart_user



class Transaction(models.Model):
    ORDERSTATUS = ( ("Pending","Pending"),("Out for Shipping","Out for Shipping"),("Completed","Completed"))
    DELIVERY_OPTION = ( ("pickup","pickup"),("delivery","delivery"))

    transaction_no =  models.CharField(unique=True, max_length=200, null=False,verbose_name='Transaction Number')
    transaction_user = models.CharField(max_length=250, null=True, verbose_name='List Username')
    transaction_fname = models.CharField(max_length=250, null=True, verbose_name='First Name') 
    transaction_lname = models.CharField(max_length=250, null=True, verbose_name='Last Name') 
    transaction_address = models.TextField(null=False, verbose_name='Address') 
    transaction_contactno = models.BigIntegerField( null=True, verbose_name='Contact Number')
    transaction_doption = models.CharField(max_length=250, choices= DELIVERY_OPTION, null=True, verbose_name='Delivery Option')
    transaction_preferred_date = models.CharField(max_length=250,  null=True,   verbose_name='Preferred Date') 
    transaction_totalprice =  models.BigIntegerField(null=True, default=0, verbose_name='Total Price')
    created_at =models.DateField(default=timezone.now,  verbose_name='Date Ordered')
    transaction_orderstatus = models.CharField(max_length=250, choices=ORDERSTATUS, null=True, default='Pending',verbose_name='Status')
    transaction_delivered = models.DateTimeField(null=True, blank=True, verbose_name='Delivered Time')

    def __str__(self):
        return self.transaction_no



class OrderItem(models.Model):
    OrderItem_transactionNo =  models.CharField(max_length=200, null=True,  verbose_name='Transaction Number')
    OrderItem_category =  models.CharField(max_length=200, verbose_name='Category')
    OrderItem_name=  models.CharField(max_length=200, verbose_name='Product Name')
    OrderItem_unit =  models.CharField(max_length=200, null=True, verbose_name='Unit')
    OrderItem_quantity =  models.CharField(max_length=200, null=True, verbose_name='quantity')
    OrderItem_amount =  models.DecimalField( max_digits=10, decimal_places=2,null=True, verbose_name='Amount')

    def __str__(self):
        return self.OrderItem_transactionNo

class Profile(models.Model):
    list_user = models.CharField(max_length=100, null=False, verbose_name="List User")
    profile_fname = models.CharField(max_length=250, null=False, verbose_name="First Name")
    profile_mname = models.CharField(max_length=250,  null=False, verbose_name="Middle Name")
    profile_lname = models.CharField(max_length=250, null=False, verbose_name="Last Name")
    profile_cnumber = models.BigIntegerField( null=False, verbose_name="Contact Number")
    profile_address = models.TextField(null=False, verbose_name="Address")
    profile_email = models.CharField( max_length=100, null=False, verbose_name="Email Address")
    profile_pic =models.ImageField( upload_to=image_path,null=True, verbose_name='Profile Pic')

    def __str__(self):
        return self.profile_email




class Activity_log(models.Model):
    user_name = models.CharField(max_length=250, verbose_name=' Username')
    activity = models.CharField(max_length=250, verbose_name='Activity')
    date_time =  models.DateTimeField(default=timezone.now, verbose_name='Date and Time')
    role = models.CharField(max_length=100, null=True,verbose_name='Role')

    def __str__(self):
        return self.activity

class Settings(models.Model):
    settings_category = models.CharField(max_length=250, null=True, verbose_name='Category')
    settings_unit = models.CharField(max_length=250, null=True, verbose_name='Unit')

    def __str__(self):
        return self.settings_category

