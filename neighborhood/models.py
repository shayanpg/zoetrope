from django.db import models
from accounts.models import Profile
from django.urls import reverse

# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length=200, help_text='e.g. Midtown, Sacramento, CA')
    points = models.TextField(help_text='''Please enter a JSON-style set of
        (lat, lon) points that define the neighborhood in clockwise order.<br>
        e.g. TODO<br>
        is Google Maps' definition of Midtown Sacramento''')
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('nhood-detail', kwargs={'pk': self.pk})
