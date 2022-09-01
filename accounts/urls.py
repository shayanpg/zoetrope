from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('calls_depleted/', views.calls_depleted, name='calls_depleted'),
]
