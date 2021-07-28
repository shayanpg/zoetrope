from django.urls import path
from . import views

urlpatterns = [
    path('', views.neighborhood, name='neighborhood'),
    path('<int:pk>/detail/', views.NeighborhoodDetailView.as_view(), name='nhood-detail'),
    path('<int:pk>/update/', views.NeighborhoodUpdateView.as_view(), name='nhood-update'),
    path('<int:pk>/delete/', views.NeighborhoodDeleteView.as_view(), name='nhood-delete'),
]
