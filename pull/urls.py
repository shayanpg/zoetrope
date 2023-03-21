from django.urls import path
from . import views

urlpatterns = [
    path('', views.history, name='history'),
    path('<int:pull_id>', views.get_pull, name="get_pull"),
]
