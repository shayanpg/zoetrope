from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='gsv-home'),
    path('about/', views.about, name='gsv-about'),
]
