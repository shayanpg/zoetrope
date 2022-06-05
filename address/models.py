from django.db import models
from neighborhood.models import Neighborhood

# Create your models here.
class Address(models.Model):
    name = models.CharField(max_length=200, help_text='e.g. 2384 Telegraph Ave, Berkeley, CA')
    lat = models.CharField(max_length=100, help_text='keep this in mind: '+'https://xkcd.com/2170/')
    lng = models.CharField(max_length=100, help_text='keep this in mind: '+'https://xkcd.com/2170/')
    neighborhoods = models.ManyToManyField(Neighborhood)

    def __str__(self):
        return self.name
