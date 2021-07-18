from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile

class ProfileCreationForm(UserCreationForm):

    class Meta:
        model = Profile
        fields = ('username', 'gsv_api', 'maps_api')

class ProfileChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('username', 'email', 'gsv_api', 'maps_api')
