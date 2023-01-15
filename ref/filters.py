from django_filters import rest_framework as filters
from .models import Building,StaticMesh

class BuildingFilter(filters.FilterSet):
    class Meta:
        model = Building
        fields = ('id_code', 'project_name','owner_id','project_process','category')

class StaticMeshFilter(filters.FilterSet):
    class Meta:
        model = StaticMesh
        fields = ('id_code', 'building_project_id','obj_name','obj_code','material')