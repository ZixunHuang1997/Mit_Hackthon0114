from django.urls import include, path
from rest_framework import routers
from .views import NotificationBoard, NewEmail


urlpatterns = [
    path("", NotificationBoard.as_view(), name="notify"), #open board #param: deep T?F
    path("mail", NewEmail.as_view(), name="email"), #send new mail #param: mailcontent
    path("unread", )

]