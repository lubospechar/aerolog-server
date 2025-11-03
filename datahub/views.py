from django.utils.dateparse import parse_datetime
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly  # upravíme za chvilku
from .models import Sensor
from .serializers import SensorSyncSerializer

class SensorSyncView(ListAPIView):
    serializer_class = SensorSyncSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Sensor.objects.all().order_by("id")

        modified_since = self.request.query_params.get("modified_since")
        if modified_since:
            dt = parse_datetime(modified_since)
            if dt is not None:
                # zajistíme, že je to aware a v UTC
                if timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone=timezone.utc)
                qs = qs.filter(updated_at__gt=dt)
        return qs