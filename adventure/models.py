from django.db import models
from importlib_metadata import distribution

import re
from datetime import date

# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self):
        passengers = self.passengers
        seats = []
        for i in range(passengers):
            if (i+1)%2 == 0:
                seats.append([True, True])
            else:
                if i+1 == passengers:
                    seats.append([True, False])
        print(seats)
        return seats


class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self):
        if self.end and self.end <= date.today():
            return True
        else:
            return False

def validate_number_plate(number_plate):
    regex = re.compile(r"[A-Z]+[A-Z]+[-]+[0-9][0-9]+[-]+[0-9][0-9]")
    if re.fullmatch(regex, number_plate):
        return True
    else:
        return False
