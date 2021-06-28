from django.urls import path
from . import views

urlpatterns = [
    path('', views.address, name='gsv-address'),
    path('response/', views.response, name='gsv-response'),
]
