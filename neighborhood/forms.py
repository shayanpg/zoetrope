from django.forms import ModelForm
from .models import Neighborhood

class NeighborhoodCreationForm(ModelForm):
    class Meta:
        model = Neighborhood
        fields = ['name', 'points']
