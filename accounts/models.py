from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
    gsv_api = models.CharField(max_length=50, blank=True)
    maps_api = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username
