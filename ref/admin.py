from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Building,StaticMesh
# Register your models here.
# admin.site.register(Building)
# admin.site.register(BuildingComponent)
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['id_code', 'project_name','owner_id','project_process','category','updated_at']

@admin.register(StaticMesh)
class StaticMeshAdmin(admin.ModelAdmin):
    list_display = ['id_code', 'building_project_id','obj_name','obj_code','material','updated_at']