from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.utils.safestring import mark_safe

class ProfileCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = Profile
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = Profile
        fields = ['username', 'email']
