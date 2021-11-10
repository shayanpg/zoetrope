from django.urls import path
from . import views

urlpatterns = [
    #/map/
    path('', views.index, name='index'),
    # /map/download_some_images
    # path('downloadSomeImages/<int:neighborhood_id>', views.download_some_images, name='downloadSomeImages'),

    #eg. /map/1
    path('<int:neighborhood_id>', views.polygon, name='polygon'),

    path('m', views.map, name="map"),

    path('draw', views.draw, name="draw"),
    ]
