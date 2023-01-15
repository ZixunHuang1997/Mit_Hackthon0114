from rest_framework import serializers
from .models import Mail

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        read_only_field = ("id_code",)
        field = '_all_'

