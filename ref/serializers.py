from rest_framework import serializers

from .models import Building,StaticMesh

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        read_only_fields = ("id_code",)
        fields = '__all__'

class StaticMeshSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticMesh
        read_only_fields = ("id_code",)
        fields = '__all__'