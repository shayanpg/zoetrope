from django.urls import path
from . import views

# TEMP: using map app index file, delete later
from map import views as mviews

urlpatterns = [
    # path('', views.sample, name='sample'),
    # TEMP: Delete following path later, uncomment last line
    path('', mviews.index, name='sample'),
]
