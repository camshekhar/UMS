from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetail(models.Model):
    uname = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.CharField(max_length=200, null=True)
    fname = models.CharField(max_length=200, null=True)
    lname = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)

