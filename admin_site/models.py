from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.safestring import mark_safe
import os, random 

now = timezone.now()
# Create your models here.



def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'valid_id/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance,basename=basefilename, randomstring=randomstr, ext = file_extension, year=now.strftime('%Y'), month= _now.strftime('%m'),day=_now.strftime('$d'))

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
    reseller_id =models.ImageField( upload_to="image_path",default="image_path/dog.jpg",verbose_name='Valid ID')
    reseller_businessp =models.ImageField( upload_to="image_path",default="image_path/dog.jpg",verbose_name='Business Permit')
    reseller_status =models.CharField(max_length=200, null=True, choices=STATUS, verbose_name='Status')

    def __image_tag__(self):
        return mark_safe('<img src="dashboard/media/%s" width="50" height="50" />'%(self.reseller_id))

    def __str__(self):
        return self.reseller_email



class Product(models.Model):
    STATUS = (("available","available"),("n/a","n/a"))
    product_code =  models.CharField(unique=True, max_length=200, verbose_name='Product Code')
    product_category =  models.CharField(max_length=200, verbose_name='Category')
    product_name=  models.CharField(max_length=200, verbose_name='Product Name')
    product_size =  models.CharField(max_length=200, verbose_name='Size')
    product_price =  models.CharField(max_length=200, verbose_name='Price')
    product_stock =  models.CharField(max_length=200, verbose_name='Available Stock')
    product_status =  models.CharField(max_length=200, choices=STATUS, verbose_name='Status')
    product_expiry =  models.DateField( null=True, default=timezone.now, verbose_name='Expiry Date')

class Pos(models.Model):
    pos_user =  models.CharField(max_length=200, null=False, default=None, verbose_name='List user')
    pos_pcode =  models.CharField(max_length=200, verbose_name='Product Code')
    pos_category =  models.CharField(max_length=200, verbose_name='Category')
    pos_name=  models.CharField(max_length=200, verbose_name='Product Name')
    pos_size =  models.CharField(max_length=200, verbose_name='Size')
    pos_price =  models.CharField(max_length=200, verbose_name='Price')
    pos_quantity =  models.CharField(max_length=200, null=True, verbose_name='quantity')
    pos_amount =  models.IntegerField(verbose_name='Amount')


class Activity_log(models.Model):
    user_name = models.CharField(max_length=250, verbose_name=' Username')
    activity = models.CharField(max_length=250, verbose_name='Activity')
    date_time =  models.DateTimeField(default=timezone.now, verbose_name='Date and Time')
    

