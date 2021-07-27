from django.forms import ModelForm
from .models import Neighborhood
from django.utils.translation import gettext_lazy as _

class NeighborhoodCreationForm(ModelForm):
    class Meta:
        model = Neighborhood
        fields = ['name', 'points']
        labels = {
            'name': _('Neighborhood Name'),
            'points': _('Bounding Points'),
        }
        error_messages = {
            'name': {
                'max_length': _("Neighborhood name is too long."),
            },
        }
