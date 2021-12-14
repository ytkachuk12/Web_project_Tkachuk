from django.db import models


# Create your models here.
class Airline(models.Model):
    code = models.IntegerField()
    ICAO = models.CharField(max_length=3)
    IATA = models.CharField(max_length=2)


class Aircraft(models.Model):
    type = models.CharField(max_length=10)
    registration = models.CharField(max_length=10)


class Flight(models.Model):
    name = models.CharField(max_length=15)
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE)
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    schedule_date_time = models.DateTimeField()
    actual_landing_time = models.DateTimeField()
    actual_off_time = models.DateTimeField()
    expected_boarding_time = models.DateTimeField()
    estimate_landing_time = models.DateTimeField()
    status = models.ManyToManyField('Status', through='FlightStatus')
    airport = models.ManyToManyField('Airport', through='FlightAirport')


class Airport(models.Model):
    name = models.CharField(max_length=3)


class FlightAirport(models.Model):
    FROM_TO_MARKER_CHOICES = [
        ('DEP', 'Departure airport'),
        ('ARR', 'Arrive airport'),
        ('TRAN', 'Transition airport')
    ]
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    airport = models.ForeignKey('Airport', on_delete=models.CASCADE)
    from_to_marker = models.CharField(max_length=4, choices=FROM_TO_MARKER_CHOICES)


class Status(models.Model):
    status = models.CharField(max_length=3)


class FlightStatus(models.Model):
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
