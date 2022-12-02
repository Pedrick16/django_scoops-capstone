from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    ROLE = ((" "," "),("admin","admin"),("staff","staff"),("reseller","reseller"),("rider","rider"))  
    role = models.CharField(max_length=50, null=True, default=False, choices=ROLE)        
