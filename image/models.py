from django.db import models
from address.models import Address
from pull.models import Pull
from PIL import Image

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='places/', default='default.jpg')
    file_path = models.TextField(max_length=200,help_text="Full path of the image, including S3 directory")
    angle = models.FloatField(max_length=10, help_text='Angle from which image was captured')
    year = models.TextField(max_length=4,help_text="Year on which image was captured")

    address_id = models.ForeignKey(Address, on_delete=models.PROTECT, null=False)
    pull_id = models.ForeignKey(Pull, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return self.file_path
