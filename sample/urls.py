from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='sample'),
    path('<int:neighborhood_id>', views.sample_points, name="sample_points"),
    path('fin/<int:neighborhood_id>/<str:sample>', views.sample_success, name="sample_success"),
]
