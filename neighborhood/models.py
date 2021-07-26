from django.db import models
from accounts.models import Profile

# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length=200)
    points = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name
