# datahub/serializers.py
from rest_framework import serializers
from datahub.models import Sensor

class SensorSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "code", "name", "unit", "updated_at"]
