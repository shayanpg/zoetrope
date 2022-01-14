from django.db import models
from accounts.models import Profile
from django.urls import reverse

# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length=200, help_text='e.g. Midtown, Sacramento, CA')
    points = models.TextField(help_text='''Please enter a JSON-style set of
        (lat, lng) points that define the neighborhood in clockwise order.<br>
        For example,<br>
        [<br>
        { "lat": 38.5782, "lng": -121.4852 },<br>
        { "lat": 38.5753, "lng": -121.4746 },<br>
        { "lat": 38.5808, "lng": -121.4722 },<br>
        { "lat": 38.5788, "lng": -121.4649 },<br>
        { "lat": 38.5645, "lng": -121.4711 },<br>
        { "lat": 38.5693, "lng": -121.4891 }<br>
        ]<br>
        is the definition Google Maps provides for Midtown Sacramento, CA.''')
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('nhood-detail', kwargs={'pk': self.pk})
