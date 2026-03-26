from core.models import AppVersion
from rest_framework import serializers

class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = ['name','version']



