from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.IntegerField(verbose_name="شماره تلفن",default=0)