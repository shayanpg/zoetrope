from django.db import models
from accounts.models import Profile

# Create your models here.
class Neighborhood(models.Model):
    name = models.CharField(max_length=200, help_text='e.g. Midtown, Sacramento, CA')
    points = models.TextField(help_text='''Please enter a comma-separated set of
        (lat, lon) points that define the neighborhood in clockwise order.<br>
        e.g. (38.578150, -121.485202), (38.575276, -121.474581), (38.580765, -121.472200),
        (38.578762, -121.464867), (38.564494, -121.471080), (38.569284, -121.489054)<br>
        is Google Maps' definition of Midtown Sacramento''')
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('nhood-detail', kwargs={'pk': self.pk})
