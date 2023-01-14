from django.urls import include, path
from rest_framework import routers
from .views import Notify


urlpatterns = [
    path("", Notify.as_view(), name="notify"),
]