# datahub/serializers.py
from rest_framework import serializers
from datahub.models import Sensor, Unit

class SensorSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "code", "name", "unit"]


class UnitSyncSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ["id", "name", "symbol"]