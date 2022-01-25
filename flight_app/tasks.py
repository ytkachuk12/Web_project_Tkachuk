"""Celery tasks:
    - weather task. get data from weather api for number of HOURS and store it in DB
    - flight task. det data from airport Schiphol api and store it in DB"""
import datetime
from celery import shared_task

from flight_app.service import FlightService
from flight_app.service_weather import WeatherService

# get data for 14 days
DAYS_AGO = 7
DAYS_AHEAD = 7
period = DAYS_AGO + DAYS_AHEAD + 1

# get forecast for 7 days
HOURS = 168


def start_day() -> datetime.date:
    """Function count date of first day of period we want to store data.
     It equal today - period days ago
        :return datetime.date"""
    today = datetime.date.today()
    difference_between_days = datetime.timedelta(days=DAYS_AGO)
    return today - difference_between_days


@shared_task
def parse_weather_task():
    """weather task"""
    parse_weather = WeatherService(HOURS)
    parse_weather.parse()
    return True


@shared_task
def parse_flights_task():
    """flight task"""
    current_day = start_day()
    for _ in range(period):
        parse_flights = FlightService(current_day)
        parse_flights.parse()
        current_day += datetime.timedelta(days=1)
    return True
