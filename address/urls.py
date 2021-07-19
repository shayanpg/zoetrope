from django.urls import path
from . import views

urlpatterns = [
    path('', views.address, name='address'),
]
