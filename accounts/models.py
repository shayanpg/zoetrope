from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Profile(AbstractUser):
    gsv_api = models.CharField(max_length=50, blank=True)
    maps_api = models.CharField(max_length=50, blank=True)
    api_calls_remaining = models.IntegerField(default=2000)

    def __str__(self):
        return self.username

    def dec_remaining_calls(self, num_calls):
        self.api_calls_remaining -= num_calls
        self.save()
