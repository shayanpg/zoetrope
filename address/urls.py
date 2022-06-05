from django.urls import path
from . import views

urlpatterns = [
    path('', views.address_form, name='address'),
]
