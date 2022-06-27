from django.urls import path
from . import views

urlpatterns = [
    path('', views.address_form, name='address'),
    path('fin/<str:address>/<str:point>', views.address_success, name='address_success'),
]
