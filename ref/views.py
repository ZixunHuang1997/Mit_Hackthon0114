#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   views.py
@Author  :   HUANG Zixun
@Version :   1.0
@Contact :   zixunhuang@outlook.com
@License :   Copyright © 2007 Free Software Foundation, Inc
@Desc    :   None
'''
import json
import os

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (generics, mixins, permissions, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .filters import BuildingFilter,StaticMeshFilter
from .models import Building,StaticMesh
from .serializers import BuildingSerializer,StaticMeshSerializer

class StaticMeshViewSet(viewsets.ModelViewSet):
    queryset = StaticMesh.objects.all()
    serializer_class = StaticMeshSerializer
    filter_class = StaticMeshFilter
    permission_classes = [permissions.AllowAny]
    def update(self, request, *args, **kwargs):
        # try: request.data['owner'] = self.request.user._wrapped.id
        # except: request.data['owner'] = self.request.user.id
        print('static_put',request.data)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    # def create(self, request, *args, **kwargs):
    #     category = request.data['category']
    #     try:
    #         with transaction.atomic():
    #             if category == 'ZPlus':
    #                 with open('media/BuildingInstanceCases/ZPlus_instance.json') as f:
    #                     instance = json.load(f)
    #                 request.data['instance'] = instance
    #                 with open('media/StaticMeshCases/ZPlus_staticMesh.json') as f:
    #                     static_mesh = json.load(f)
    #                 request.data['static_mesh'] = static_mesh
                
    #             serializer = self.get_serializer(data=request.data) 
    #             serializer.is_valid(raise_exception=True)

    #             # print(serializer.data)
    #             self.perform_create(serializer)
    #             headers = self.get_success_headers(serializer.data)
    #             # print(serializer)
    #             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     except Exception as e:
    #         raise APIException(str(e))
def static_mesh_updating(request):
    # print('request.body:',json.loads(request.body))cd n
    try:
        with transaction.atomic():
            building_info = json.loads(request.body)
            building_id = building_info['building_id']
            # print(building_id)
            # print(type(building_id))
            building_instance = Building.objects.get(id_code = building_id)
            static_list = StaticMesh.objects.filter(building_project_id = building_id).order_by('id_code')
            static_category = []
            for static_item in static_list:
                serialized_mesh0 = StaticMeshSerializer(static_item).data
                serialized_mesh0['building_project_id'] = str(serialized_mesh0['building_project_id'])
                serialized_mesh0.pop('building_project_id')
                serialized_mesh0.pop('updated_at')
                serialized_mesh0.pop('created_at')
                # new_static_mesh.append(serialized_mesh0)
                static_category.append(serialized_mesh0)
            building_instance.static_mesh = static_category
            building_instance.save()
    except Exception as e:
        raise APIException(str(e))
    return JsonResponse({
        'status': status.HTTP_200_OK,
        'building_id': building_instance.id_code,
        'static_mesh': building_instance.static_mesh,
        'instance': building_instance.instance,
    })


def box_initializing(request):
    # print()
    print('request.body:',json.loads(request.body))
    try:
        with transaction.atomic():
            building_info = json.loads(request.body)
            category = building_info['category']
            
            if category == 'ZPlus':
                with open('media/BuildingInstanceCases/structure1220.json',encoding='UTF-8') as f:
                    instance = json.load(f)
                with open('media/StaticMeshCases/canseestill.json',encoding='UTF-8') as f:
                    static_mesh = json.load(f)
            building_instance = Building(
                project_name = building_info['project_name'],
                category = category,
                instance = instance,
                static_mesh = static_mesh,
            )
            building_instance.save()
            new_static_mesh = []
            for mesh in static_mesh:
                mesh0 = StaticMesh(
                    building_project_id = building_instance,
                    obj_name = mesh['obj_name'],
                    obj_code = mesh['obj_code'],
                    x = mesh['x'],
                    y = mesh['y'],
                    z = mesh['z'],
                    rx = mesh['rx'],
                    ry = mesh['ry'],
                    rz = mesh['rz'],
                    angle = mesh['angle'],
                    ui_name = mesh['UI_code'],
                    material = mesh['material'],
                )
                mesh0.save()
                serialized_mesh0 = StaticMeshSerializer(mesh0).data
                serialized_mesh0['building_project_id'] = str(serialized_mesh0['building_project_id'])
                serialized_mesh0.pop('building_project_id')
                serialized_mesh0.pop('updated_at')
                serialized_mesh0.pop('created_at')
                new_static_mesh.append(serialized_mesh0)
            # building_instance.static_mesh = new_static_mesh
            # print(StaticMeshSerializer(mesh0).data)
            # print(serializer.data['static_mesh'][0]['Name'])
            # print(serializer.data['static_mesh'][0]['x'])
            # print(serializer.data['static_mesh'][0]['y'])
            # print(serializer.data['static_mesh'][0]['z'])
            # print(serializer.data['static_mesh'][0]['rx'])
            # print(serializer.data['static_mesh'][0]['ry'])
            # print(serializer.data['static_mesh'][0]['rz'])
            # print(serializer.data['static_mesh'][0]['angle'])
            # print(serializer.data['static_mesh'][0]['material'])
            # print(serializer.data['static_mesh'][0]['UI_name'])
            # print(serializer.data['static_mesh'][0]['CID'])
            print(serialized_mesh0)
            building_instance.static_mesh = new_static_mesh
            building_instance.save()
    except Exception as e:
        raise APIException(str(e))
    return JsonResponse({
        'status': status.HTTP_200_OK,
        'building_id': building_instance.id_code,
        'static_mesh': building_instance.static_mesh,
        'instance': building_instance.instance,
    })

class BuildingViewSet(
    mixins.RetrieveModelMixin,
    # mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    # mixins.DestroyModelMixin,
    mixins.CreateModelMixin):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filter_class = BuildingFilter
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        category = request.data['category']
        try:
            with transaction.atomic():
                if category == 'ZPlus':
                    with open('media/BuildingInstanceCases/002instacelzt.json',encoding='UTF-8') as f:
                        instance = json.load(f)
                    request.data['instance'] = instance
                    with open('media/StaticMeshCases/002UIlzt.json',encoding='UTF-8') as f:
                        static_mesh = json.load(f)
                    request.data['static_mesh'] = static_mesh

                serializer = self.get_serializer(data=request.data) 
                serializer.is_valid(raise_exception=True)
                # print(serializer.data)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                # print(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            raise APIException(str(e))

    # def perform_create(self, serializer):
        # print('create singlebox:', serializer)
        # try:
        #     with transaction.atomic():
        #         for static_mesh in serializer.data['static_mesh']:
        #             mesh = StaticMesh( obj_name = static_mesh['Name'])

                # print(serializer.data['static_mesh'][0]['Name'])
                # print(serializer.data['static_mesh'][0]['x'])
                # print(serializer.data['static_mesh'][0]['y'])
                # print(serializer.data['static_mesh'][0]['z'])
                # print(serializer.data['static_mesh'][0]['rx'])
                # print(serializer.data['static_mesh'][0]['ry'])
                # print(serializer.data['static_mesh'][0]['rz'])
                # print(serializer.data['static_mesh'][0]['angle'])
                # print(serializer.data['static_mesh'][0]['material'])
                # print(serializer.data['static_mesh'][0]['UI_name'])
                # print(serializer.data['static_mesh'][0]['CID'])

        # except Exception as e:
        #     raise APIException(str(e))

    # def get_queryset(self):
    #     # category = self.request.GET.get('category', None)
    #     qs = super(BuildingViewSet, self).get_queryset()
    #     return qs

        # if category:
        #     qs = qs.filter(category = category)
        #     if self.request.user.is_superuser:
        #         return qs
        #     return  Building.objects.filter(owner=self.request.user).filter(category = category).order_by('updated_at')
        # else:
        #     if self.request.user.is_superuser:
        #         return qs
        #     return Building.objects.filter(owner=self.request.user).order_by('updated_at')

    # def get(self, request, *args, **kwargs):
        # return self.list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     try: request.data['owner'] = self.request.user._wrapped.id
    #     except: request.data['owner'] = self.request.user.id
    #     try:
    #         with transaction.atomic():
    #             request.data['prediction_model'] = Endpoint.objects.\
    #             filter(name = request.data['prediction_model'])[0].id
    #     except Exception as e:
    #         return Response(
    #             {"status": "Error", 
    #              "message": "ML algorithm is not available"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     serializer = self.get_serializer(data=request.data)
    #     print(serializer)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
        
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # try: request.data['owner'] = self.request.user._wrapped.id
        # except: request.data['owner'] = self.request.user.id
        # print(request.data)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# # Create your views here.
# class BuildingViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = Building.objects.all().order_by('id_code')
#     serializer_class = BuildingSerializer
#     filter_class = BuildingFilter
#     # permission_classes = [permissions.IsAuthenticated]
#     permission_classes = [permissions.AllowAny]
#     # filter_backends = [DjangoFilterBackend]
#     # filterset_fields = '__all__'
#     def get_queryset(self):
#         qs = super(BuildingViewSet, self).get_queryset()
#         return
#         if self.request.user.is_superuser:
#             return qs
#         return Building.objects.filter(user=self.request.user).order_by('update_at')

#     def get(self, request, *args, **kwargs):
#         # print(request.user._wrapped.id)
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         # category = self.request.query_params.get("status", "production")
#         return self.create(request, *args, **kwargs)
    # def put(self,request,*args,**kwargs):
    #     return self.update(request)
    # def delete(self,request,*args,**kwargs):
    #     print(request.user._wrapped.id)
    #     return self.destroy(request)
    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #     print(self.request.GET.get('category'))
    #    
        
    #     serializer = self.get_serializer(data=request.data) 
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     # print(serializer)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



































# from django.db import transaction
# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# from mlendpoint.models import Endpoint
# from rest_framework import generics, mixins, permissions, status, viewsets
# from rest_framework.exceptions import APIException
# from rest_framework.response import Response

# from .filters import BuildingFilter
# from .models import Building
# from .serializers import BuildingSerializer

# # Create your views here.
# class BuildingViewSet(
#     mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,
#     mixins.UpdateModelMixin,mixins.DestroyModelMixin):
#     queryset = Building.objects.all().order_by('owner')
#     serializer_class = BuildingSerializer
#     filter_class = BuildingFilter
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         category = self.request.GET.get('category', None)
#         qs = super(BuildingViewSet, self).get_queryset()

#         if category:
#             qs = qs.filter(category = category)
#             if self.request.user.is_superuser:
#                 return qs
#             return  Building.objects.filter(owner=self.request.user).filter(category = category).order_by('updated_at')
#         else:
#             if self.request.user.is_superuser:
#                 return qs
#             return Building.objects.filter(owner=self.request.user).order_by('updated_at')

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     # def create(self, request, *args, **kwargs):
#     #     try: request.data['owner'] = self.request.user._wrapped.id
#     #     except: request.data['owner'] = self.request.user.id
#     #     try:
#     #         with transaction.atomic():
#     #             request.data['prediction_model'] = Endpoint.objects.\
#     #             filter(name = request.data['prediction_model'])[0].id
#     #     except Exception as e:
#     #         return Response(
#     #             {"status": "Error", 
#     #              "message": "ML algorithm is not available"},
#     #             status=status.HTTP_400_BAD_REQUEST,
#     #         )

#     #     serializer = self.get_serializer(data=request.data)
#     #     print(serializer)
#     #     serializer.is_valid(raise_exception=True)
#     #     self.perform_create(serializer)
#     #     headers = self.get_success_headers(serializer.data)
        
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

#     def update(self, request, *args, **kwargs):
#         # try: request.data['owner'] = self.request.user._wrapped.id
#         # except: request.data['owner'] = self.request.user.id
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)
