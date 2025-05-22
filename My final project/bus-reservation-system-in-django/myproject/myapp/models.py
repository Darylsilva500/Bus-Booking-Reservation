# Create your models here.
from django.db import models


# Create your models here.

from django.db import models

from django.db import models

from django.db import models

class Bus(models.Model):
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    # Weekly schedule - for each day, date and time of the bus
    monday_date = models.DateField(null=True, blank=True)
    monday_time = models.TimeField(null=True, blank=True)

    tuesday_date = models.DateField(null=True, blank=True)
    tuesday_time = models.TimeField(null=True, blank=True)

    wednesday_date = models.DateField(null=True, blank=True)
    wednesday_time = models.TimeField(null=True, blank=True)

    thursday_date = models.DateField(null=True, blank=True)
    thursday_time = models.TimeField(null=True, blank=True)

    friday_date = models.DateField(null=True, blank=True)
    friday_time = models.TimeField(null=True, blank=True)

    saturday_date = models.DateField(null=True, blank=True)
    saturday_time = models.TimeField(null=True, blank=True)

    sunday_date = models.DateField(null=True, blank=True)
    sunday_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.bus_name} ({self.source} to {self.dest})"




class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Book(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    busid=models.DecimalField(decimal_places=0, max_digits=2)
    bus_name = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    dest = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=2)

    def __str__(self):
        return self.email
