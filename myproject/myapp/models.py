from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=250, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255,unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

    