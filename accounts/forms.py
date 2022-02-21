from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.utils.safestring import mark_safe

class ProfileCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gsv_api'].required = True
        self.fields['maps_api'].required = True
        self.fields['email'].required = True

        self.fields['gsv_api'].label = "Google Street View API Key"
        self.fields['maps_api'].label = "Google Maps API Key"

        self.fields['gsv_api'].help_text = mark_safe(
            "Don't have an API key? Learn how to get one " +
            "<a href=https://developers.google.com/maps/documentation/streetview/get-api-key target=_blank>here</a>." +
            "Note: be sure to enable the 'Street View Static API' for this key."
        )
        self.fields['maps_api'].help_text = mark_safe(
            "Don't have an API key? Learn how to get one " +
            "<a href=https://developers.google.com/maps/documentation/geocoding/start target=_blank>here</a>." +
            "Note: be sure to enable both the 'Geocoding API' and the 'Maps JavaScript API' for this key."
        )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'gsv_api', 'maps_api']

class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['gsv_api'].required = True
        self.fields['maps_api'].required = True
        self.fields['email'].required = True

        self.fields['gsv_api'].label = "Google Street View API Key"
        self.fields['maps_api'].label = "Google Maps API Key"

        self.fields['gsv_api'].help_text = mark_safe(
            "Don't have an API key? Learn how to get one " +
            "<a href=https://developers.google.com/maps/documentation/streetview/get-api-key target=_blank>here</a>."
        )
        self.fields['maps_api'].help_text = mark_safe(
            "Don't have an API key? Learn how to get one " +
            "<a href=https://developers.google.com/maps/documentation/geocoding/start target=_blank>here</a>."
        )

    class Meta:
        model = Profile
        fields = ['username', 'email', 'gsv_api', 'maps_api']
