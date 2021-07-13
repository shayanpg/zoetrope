from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileCreationForm, ProfileChangeForm
from .models import Profile

class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm
    form = ProfileChangeForm
    model = Profile
    list_display = ['email', 'username', 'gsv_api', 'maps_api']

admin.site.register(Profile, ProfileAdmin)
