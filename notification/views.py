# Create your views here.
from django.shortcuts import render
from rest_framework import (generics, mixins, permissions, status, views,
                            viewsets)
from rest_framework.response import Response


# Create your views here.
def openNotification():
    print('openNotification!')
def mailSend():
    print('mailSend!')
def openDoc():
    print('openDoc!')


class Notify(views.APIView):
    def post(self, request, format=None):
        print(request.data)
        openNotification()
        return Response(status=status.HTTP_201_CREATED)

class Email(views.APIView):
    def post(self, request, format=None):
        print(request.data)
        mailSend()
        return Response(status=status.HTTP_201_CREATED)
