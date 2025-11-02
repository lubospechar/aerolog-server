from django.db import models

class Station(models.Model):
    name = models.CharField(
        max_length=100,
    )
    latitude = models.FloatField()
    longitude = models.FloatField()

    ip = models.GenericIPAddressField(
        protocol='ipv4',
        null=False,
        blank=False,
        unique=True
    )


class Unit(models.Model):
    name = models.CharField(
        max_length=100,
    )
    symbol = models.CharField(
        max_length=10,
    )

    def __str__(self) -> str:
        if self.symbol:
            return f"{self.name} ({self.symbol})"
        return self.name


class Sensor(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(
        max_length=100,
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} [{self.code}]"


class Measure(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"{self.sensor.code} @ {self.timestamp:%Y-%m-%d %H:%M:%S} = {self.value}"