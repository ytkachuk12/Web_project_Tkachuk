from django.db import models


# Create your models here.
class Airline(models.Model):
    code = models.IntegerField(unique=True)
    ICAO = models.CharField(max_length=3, null=True)
    IATA = models.CharField(max_length=2)

    class Meta:
        """Index for Airline
            - search for code, IATA
            - search for code"""
        indexes = [models.Index(fields=['code', 'IATA'])]


class Aircraft(models.Model):
    type = models.CharField(max_length=10)
    registration = models.CharField(max_length=10)

    class Meta:
        """Index for Aircraft
            - search for registration, type
            - search for registration"""
        indexes = [models.Index(fields=['registration', 'type'])]


class Flight(models.Model):
    name = models.CharField(max_length=15)
    last_update = models.DateTimeField()
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE)
    aircraft = models.ForeignKey('Aircraft', on_delete=models.CASCADE)
    schedule_date_time = models.DateTimeField()
    actual_landing_time = models.DateTimeField(null=True)
    actual_off_time = models.DateTimeField(null=True)
    expected_boarding_time = models.DateTimeField(null=True)
    estimate_landing_time = models.DateTimeField(null=True)
    status = models.ManyToManyField('Status', through='FlightStatus')
    airport = models.ManyToManyField('Airport', through='FlightAirport')

    class Meta:
        """Index for Flight
                    - search for date, period(schedule_date_time field)
                    - search for name"""
        indexes = [models.Index(fields=['schedule_date_time']),
                   models.Index(fields=['name'])]


class Airport(models.Model):
    name = models.CharField(max_length=3, unique=True)
    city = models.CharField(max_length=127, null=True)
    country = models.CharField(max_length=127, null=True)
    public_name = models.CharField(max_length=127, null=True)

    class Meta:
        """Index for Airport
            - search for name"""
        indexes = [models.Index(fields=['name'])]


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
    """Status model has some data by default. Data created during migration
    Look 0002_add_data_into_Status_model.py

    No need to create index on Status because table contains less than 20 statuses"""
    name = models.CharField(max_length=3, unique=True)


class FlightStatus(models.Model):
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    status = models.ForeignKey('Status', on_delete=models.CASCADE)


class Weather(models.Model):
    datetime = models.DateTimeField()
    wind_cdir_full = models.CharField(max_length=20, verbose_name='wind direction')
    wind_spd = models.FloatField(verbose_name='wind speed')
    temp = models.FloatField(verbose_name='temperature')
    precip = models.IntegerField(verbose_name='precipitation, mm')
    snow = models.IntegerField()
    rh = models.IntegerField(verbose_name='relative humidity, %')
    clouds = models.IntegerField(verbose_name='cloud coverage, %')

    class Meta:
        """Index for Weather
            - search for datetime"""
        indexes = [models.Index(fields=['datetime'])]
