from rest_framework import serializers
from .models import Mail

class UnreadMailSerializer(serializers.ModelSerializers):
    class Meta:
        model = Mail
        read_only_field = ("id_code",)
        field = '_all_'

