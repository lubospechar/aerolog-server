# admin.py (v tvé Django aplikaci)
from django.contrib import admin
from django.db.models import Count, Max
from .models import Station, Unit, Sensor, Measure


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "ip", "latitude", "longitude", "measure_count", "last_measure_at")
    search_fields = ("name", "ip")
    ordering = ("name",)
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _measure_count=Count("measure"),
            _last_ts=Max("measure__timestamp"),
        )

    @admin.display(ordering="_measure_count", description="Počet měření")
    def measure_count(self, obj):
        return obj._measure_count

    @admin.display(ordering="_last_ts", description="Poslední měření")
    def last_measure_at(self, obj):
        return obj._last_ts


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol", "sensor_count")
    search_fields = ("name", "symbol")
    ordering = ("name",)
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_sensor_count=Count("sensor"))

    @admin.display(ordering="_sensor_count", description="Počet senzorů")
    def sensor_count(self, obj):
        return obj._sensor_count


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "unit", "measure_count", "last_measure_at")
    search_fields = ("name", "code")
    list_filter = ("unit",)
    ordering = ("name",)
    list_per_page = 50
    autocomplete_fields = ("unit",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _measure_count=Count("measure"),
            _last_ts=Max("measure__timestamp"),
        )

    @admin.display(ordering="_measure_count", description="Počet měření")
    def measure_count(self, obj):
        return obj._measure_count

    @admin.display(ordering="_last_ts", description="Poslední měření")
    def last_measure_at(self, obj):
        return obj._last_ts


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "station", "sensor", "unit", "value")
    list_filter = ("station", "sensor")
    search_fields = ("sensor__code", "sensor__name", "station__name", "station__ip")
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)
    list_select_related = ("station", "sensor", "sensor__unit")
    autocomplete_fields = ("station", "sensor")
    readonly_fields = ("timestamp",)
    list_per_page = 50

    @admin.display(ordering="sensor__unit__name", description="Jednotka")
    def unit(self, obj):
        return obj.sensor.unit

