from django.urls import path
from . import views

urlpatterns = [
    path('', views.MapFormView.as_view(), name='map'),
]
