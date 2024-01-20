from django.db import models
from datetime import timedelta


class Line(models.Model):
    name = models.CharField(max_length=10)
    status = models.CharField(max_length=10, default="Available")  # Available or Occupied


class Train(models.Model):
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    max_weight = models.FloatField()
    max_volume = models.FloatField()
    lines = models.ManyToManyField(Line)
    status = models.CharField(max_length=10, default="Available")  # Available, Booked, or Inactive
    current_weight = models.FloatField(default=0.0)
    current_volume = models.FloatField(default=0.0)
    maintenance_check = models.DateTimeField(null=True, blank=True)

    def needs_maintenance(self):
        if self.maintenance_check:
            return self.maintenance_check > timedelta(hours=3)
        return False


class Parcel(models.Model):
    weight = models.FloatField()
    volume = models.FloatField()
    status = models.CharField(max_length=10, default="Pending")  # Pending, Shipped, or Withdrawn
    owner_id = models.IntegerField()  # Assuming an identifier for the parcel owner


class Booking(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
