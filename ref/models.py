import random
import string
import uuid

from authsys.models import CustomUser
from django.db import models


def ZeroPosition():
    return {
        'x':  0,
        'y':  0,
        'z':  0,
        'rx': 0,
        'ry': 0,
        'rz': 0,
    }

# Create your models here.
class Building(models.Model):
    id_code = models.CharField(verbose_name='Building_id', primary_key=True, max_length = 50, default=uuid.uuid4, editable=False, auto_created=True)
    owner_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    project_name = models.CharField(max_length=128, default = 'Untitled')
    project_process = models.CharField(max_length=128, default = 'Under Review')
    category = models.CharField(max_length=128, default = 'ZPlus')
    instance = models.JSONField(null=True)
    static_mesh = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    def __str__(self):
        return self.project_name

# class BuildingComponent(models.Model):
#     #uuid
#     id_code = models.CharField(verbose_name='component_id', primary_key=True, max_length = 50, default=uuid.uuid4, editable=False, auto_created=True)
#     building_project_id = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
#     #obj_identification
#     obj_name = models.CharField(max_length=128, default = 'unsorted')
#     obj_type = models.BooleanField(default = False)#instance or static mesh
    
#     #obj_coor
#     # current_xyz_rxyz = models.JSONField(default=ZeroPosition)
#     x1 = models.FloatField(null=True)
#     y1 = models.FloatField(null=True)
#     z1 = models.FloatField(null=True)
#     x2 = models.FloatField(null=True)
#     y2 = models.FloatField(null=True)
#     z2 = models.FloatField(null=True)
#     rx = models.FloatField(null=True)
#     ry = models.FloatField(null=True)
#     rz = models.FloatField(null=True)
#     angle = models.FloatField(null=True)

#     #obj_attributes
#     widget_related = models.CharField(max_length=50, null=True)
#     material = models.CharField(max_length = 50, null=True)
#     # is_display = models.BooleanField(default=True)
#     def __str__(self):
#         return self.obj_name
# # class MaterialObj(models.Model):

# class InstanceComponent(models.Model):
#     #uuid
#     id_code = models.CharField(verbose_name='component_id', primary_key=True, max_length = 50, default=uuid.uuid4, editable=False, auto_created=True)
#     building_project_id = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
#     #obj_identification
#     obj_name = models.CharField(max_length=128, default = 'unsorted')
#     obj_type = models.BooleanField(default = False)#instance or static mesh
    
#     #obj_coor
#     # current_xyz_rxyz = models.JSONField(default=ZeroPosition)
#     x1 = models.FloatField(null=True)
#     y1 = models.FloatField(null=True)
#     z1 = models.FloatField(null=True)
#     x2 = models.FloatField(null=True)
#     y2 = models.FloatField(null=True)
#     z2 = models.FloatField(null=True)
#     rx = models.FloatField(null=True)
#     ry = models.FloatField(null=True)
#     rz = models.FloatField(null=True)
#     angle = models.FloatField(null=True)

#     #obj_attributes
#     widget_related = models.CharField(max_length=50, null=True)
#     material = models.CharField(max_length = 50, null=True)
#     # is_display = models.BooleanField(default=True)
#     def __str__(self):
#         return self.obj_name
# # class MaterialObj(models.Model):

class StaticMesh(models.Model):
    #uuid
    id_code = models.CharField(verbose_name='component_id', primary_key=True, max_length = 50, default=uuid.uuid4, editable=False, auto_created=True)
    building_project_id = models.ForeignKey(Building, on_delete=models.CASCADE, null=True)
    #obj_identification
    obj_name = models.CharField(max_length=128, default = 'unknown')
    obj_code = models.CharField(max_length=128, default = 'unknown')
    # row_name = models.IntegerField()
    # obj_type = models.BooleanField(default = False)#instance or static mesh
    
    #obj_coor
    # current_xyz_rxyz = models.JSONField(default=ZeroPosition)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)
    # x2 = models.FloatField(null=True)
    # y2 = models.FloatField(null=True)
    # z2 = models.FloatField(null=True)
    rx = models.FloatField(null=True)
    ry = models.FloatField(null=True)
    rz = models.FloatField(null=True)
    angle = models.FloatField(null=True)

    #obj_attributes
    ui_name = models.CharField(max_length=50, null=True)
    material = models.CharField(max_length = 50, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    # is_display = models.BooleanField(default=True)
    def __str__(self):
        return self.obj_name
# class MaterialObj(models.Model):