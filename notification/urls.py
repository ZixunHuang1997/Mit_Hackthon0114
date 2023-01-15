from django.urls import include, path
from rest_framework import routers
from .views import Notify, Email


urlpatterns = [
    path("", Notify.as_view(), name="notify"),
    path("mail", Email.as_view(), name="email"),
]