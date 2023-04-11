from django.urls import path
from . import views

urlpatterns = [
    path('', views.neighborhood_index, name='sample'),
    path('stratselect/<int:neighborhood_id>', views.strategy_index, name="strategy_index"),
    path('<int:neighborhood_id>/<str:strategy_name>', views.sample_points, name="sample_points"),
    path('fin/<int:neighborhood_id>/<str:strategy_name>/<str:sample>', views.sample_success, name="sample_success"),
]
