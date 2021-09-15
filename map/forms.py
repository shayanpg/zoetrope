from django import forms
from .models import Map
from django_google_maps.widgets import GoogleMapsAddressWidget

class MapForm(forms.ModelForm):

    class Meta(object):
        model = Map
        fields = ['address', 'geolocation']
        widgets = {
            "address": GoogleMapsAddressWidget,
        }
