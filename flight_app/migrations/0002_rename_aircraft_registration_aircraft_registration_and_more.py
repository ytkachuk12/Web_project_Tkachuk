# Generated by Django 4.0 on 2021-12-13 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aircraft',
            old_name='aircraft_registration',
            new_name='registration',
        ),
        migrations.RenameField(
            model_name='aircraft',
            old_name='aircraft_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='airline',
            old_name='airline_IATA',
            new_name='IATA',
        ),
        migrations.RenameField(
            model_name='airline',
            old_name='airline_ICAO',
            new_name='ICAO',
        ),
        migrations.RenameField(
            model_name='airline',
            old_name='airline_code',
            new_name='code',
        ),
        migrations.RenameField(
            model_name='airport',
            old_name='airport_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='flight_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='airport',
            name='flight_airport',
        ),
        migrations.RemoveField(
            model_name='status',
            name='flight_status',
        ),
        migrations.AddField(
            model_name='flight',
            name='airport_flight',
            field=models.ManyToManyField(through='flight_app.FlightAirport', to='flight_app.Airport'),
        ),
        migrations.AddField(
            model_name='flight',
            name='status_flight',
            field=models.ManyToManyField(through='flight_app.FlightStatus', to='flight_app.Status'),
        ),
    ]