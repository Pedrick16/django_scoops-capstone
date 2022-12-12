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
    reseller_address =models.CharField(max_length=200, verbose_name='Address')
    reseller_email =models.EmailField(unique=True, max_length=200, verbose_name='Email')
    reseller_id =models.ImageField( upload_to=image_path, verbose_name='valid id')
    reseller_businessp =models.ImageField( upload_to=image_path,verbose_name='business id')
    reseller_status =models.CharField(max_length=200, null=True, choices=STATUS, verbose_name='Status')


    def __str__(self):
        return self.reseller_email

   



class Product(models.Model):
    STATUS = (("available","available"),("n/a","n/a"))
    product_code =  models.CharField(unique=True, max_length=200, verbose_name='Product Code')
    product_category =  models.CharField(max_length=200, verbose_name='Category')
    product_name=  models.CharField(max_length=200, verbose_name='Product Name')
    product_size =  models.CharField(max_length=200, verbose_name='Size')
    product_price =  models.FloatField( null=True, verbose_name='Price')
    product_stock =  models.CharField(max_length=200, verbose_name='Available Stock')
    product_status =  models.CharField(max_length=200, choices=STATUS, verbose_name='Status')
    product_expiry =  models.DateField( null=True, default=None, verbose_name='Expiry Date')

    def __str__(self):
        return self.product_code

class Pos(models.Model):
    pos_user =  models.CharField(max_length=200, null=False, default=None, verbose_name='List user')
    pos_pcode =  models.CharField(max_length=200, verbose_name='Product Code')
    pos_category =  models.CharField(max_length=200, verbose_name='Category')
    pos_name=  models.CharField(max_length=200, verbose_name='Product Name')
    pos_size =  models.CharField(max_length=200, verbose_name='Size')
    pos_price =  models.FloatField( null=True, verbose_name='Price')
    pos_quantity =  models.CharField(max_length=200, null=True, verbose_name='quantity')
    pos_amount =  models.FloatField( null=True,verbose_name='Amount')

    def __str__(self):
        return self.pos_user

   


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
    transaction_totalprice = models.FloatField( null=True, verbose_name='Total Price')
    created_at =models.DateTimeField(default=timezone.now)
    transaction_orderstatus = models.CharField(max_length=250, choices=ORDERSTATUS, null=True, default='Pending',verbose_name='Status')
    transaction_delivered = models.DateTimeField(null=True, blank=True, verbose_name='Delivered Time')

    def __str__(self):
        return self.transaction_no


  



class OrderItem(models.Model):
    OrderItem_transactionNo =  models.CharField(max_length=200, null=True,  verbose_name='Transaction Number')
    OrderItem_user =  models.CharField(max_length=200, null=False, default=None, verbose_name='List Username')
    OrderItem_category =  models.CharField(max_length=200, verbose_name='Category')
    OrderItem_name=  models.CharField(max_length=200, verbose_name='Product Name')
    OrderItem_size =  models.CharField(max_length=200, verbose_name='Size')
    OrderItem_quantity =  models.CharField(max_length=200, null=True, verbose_name='quantity')
    OrderItem_amount =  models.FloatField( null=True,verbose_name='Amount')

    def __str__(self):
        return self.OrderItem_user



class Activity_log(models.Model):
    user_name = models.CharField(max_length=250, verbose_name=' Username')
    activity = models.CharField(max_length=250, verbose_name='Activity')
    date_time =  models.DateTimeField(default=timezone.now, verbose_name='Date and Time')

    def __str__(self):
        return self.user_name


    

