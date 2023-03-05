from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE = ((" "," "),("admin","admin"),("staff","staff"),("reseller","reseller"),("rider","rider"))  
    STAT = ((" "," "),("active","active"),("inactive","inactive"))
    role = models.CharField(max_length=50, null=True, default=None, choices=ROLE)
    status = models.CharField(max_length=50, null=True, default=None , choices=STAT)
