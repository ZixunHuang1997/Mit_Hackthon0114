# Create your views here.
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import (generics, mixins, permissions, status, views,
                            viewsets)
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import Mail
from rest_framework.exceptions import APIException


# Create your views here.
def openNotification():
    print('openNotification!')
def openNotification_deep():
    print('openNotification!Deep!')

def mailSend(subject='A cool subject',
             message='A stunning message'): #postman-->backend-->database
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.RECIPIENT_ADDRESS])
    print('mailSend!')

def unreadMailInfo(readall=False): # return num of mails; content of mails;
    unreads = Mail.objects.filter(unread = True).order_by('id_code')
    if readall:
        try:
            with transaction.atomic():
                for item in unreads:
                    item.unread = False
                    item.save()
        except Exception as e:
            raise APIException(str(e))


# def checkNewMail():


class Notify(views.APIView):
    def post(self, request, format=None):
        print(request.data)
        if request.data.get('deep', False):
            openNotification()
        else: 
            openNotification_deep()
        return JsonResponse({'status': status.HTTP_200_OK})

class Email(views.APIView):
    def post(self, request, format=None):
        # send email
        print(request.data)
        subject = request.data.get('subject','Untitled')
        message = request.data.get('message','Empty Message')
        mailSend(subject=subject, message=message)
        # build database
        try:
            with transaction.atomic():
                mail_item = Mail(
                    name = subject,
                    content = message,
                    unread = True,
                )
                print("model creating!")
        except Exception as e:
            raise APIException(str(e))
        return JsonResponse({
            'status': status.HTTP_200_OK,
            'id': mail_item.id_code,
            'subject': mail_item.name,
            'message': mail_item.content,
            'unread': mail_item.unread,
        })



# class MailViewSet(
#     mixins.RetrieveModelMixin,
#     # mixins.ListModelMixin,
#     viewsets.GenericViewSet,
#     mixins.UpdateModelMixin,
#     # mixins.DestroyModelMixin,
#     mixins.CreateModelMixin):
#     queryset = Mail.objects.all()
#     serializer_class = MailSerializer
#     filter_class = MailFilter
#     permission_classes = [permissions.AllowAny]

#     def create(self, request, *args, **kwargs):
#         category = request.data['category']
#         try:
#             with transaction.atomic():
#                 if category == 'ZPlus':
#                     with open('media/MailInstanceCases/002instacelzt.json',encoding='UTF-8') as f:
#                         instance = json.load(f)
#                     request.data['instance'] = instance
#                     with open('media/StaticMeshCases/002UIlzt.json',encoding='UTF-8') as f:
#                         static_mesh = json.load(f)
#                     request.data['static_mesh'] = static_mesh

#                 serializer = self.get_serializer(data=request.data) 
#                 serializer.is_valid(raise_exception=True)
#                 # print(serializer.data)
#                 self.perform_create(serializer)
#                 headers = self.get_success_headers(serializer.data)
#                 # print(serializer)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         except Exception as e:
#             raise APIException(str(e))