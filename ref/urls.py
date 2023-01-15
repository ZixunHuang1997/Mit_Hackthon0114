from django.conf.urls import include, url
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BuildingViewSet,StaticMeshViewSet,box_initializing,static_mesh_updating

router = DefaultRouter()#trailing_slash=False)
router.register(r"singlebox", BuildingViewSet, basename="building")
router.register(r"static_mesh", StaticMeshViewSet, basename="static_mesh")


urlpatterns = [
    path('', include(router.urls)),
    path('initialize/', box_initializing),
    path('update/', static_mesh_updating)
]