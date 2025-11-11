from django.utils.dateparse import parse_datetime
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datahub.models import Sensor, Unit
from datahub.serializers import SensorSyncSerializer, UnitSyncSerializer

class SensorSyncView(ListAPIView):
    serializer_class = SensorSyncSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Sensor.objects.all().order_by("id")

        modified_since = self.request.query_params.get("modified_since")
        if modified_since:
            dt = parse_datetime(modified_since)
            if dt is not None:
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone=timezone.utc)
                qs = qs.filter(updated_at__gt=dt)
        return qs


class UnitSyncView(ListAPIView):
    serializer_class = UnitSyncSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Unit.objects.all().order_by("id")

        modified_since = self.request.query_params.get("modified_since")
        if modified_since:
            dt = parse_datetime(modified_since)
            if dt is not None:
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone=timezone.utc)
                qs = qs.filter(updated_at__gt=dt)
        return qs