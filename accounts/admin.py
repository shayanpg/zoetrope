from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileCreationForm, ProfileUpdateForm
from .models import Profile

class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm
    form = ProfileUpdateForm
    model = Profile
    list_display = ['email', 'username', 'gsv_api', 'maps_api', 'api_calls_remaining']

admin.site.register(Profile, ProfileAdmin)
