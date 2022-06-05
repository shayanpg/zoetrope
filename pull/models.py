from django.db import models
from address.models import Address
from neighborhood.models import Neighborhood
from accounts.models import Profile

# Create your models here.
class Pull(models.Model):
    #num_images = models.IntegerField(max_length=10,help_text="Number of images associated the pull")
    date = models.DateField(verbose_name="Date on which pull was done")
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, null=False)
    address_id = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    neighborhood_id = models.ForeignKey(Neighborhood, on_delete=models.PROTECT, null=True)

