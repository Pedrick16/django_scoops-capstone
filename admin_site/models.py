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
    reseller_id =models.ImageField( upload_to="image_path",default="image_path/dog.jpg")
    reseller_status =models.CharField(max_length=200, null=True, choices=STATUS, verbose_name='Status')

    def __image_tag__(self):
        return mark_safe('<img src="dashboard/media/%s" width="50" height="50" />'%(self.reseller_id))

    def __str__(self):
        return self.reseller_email

