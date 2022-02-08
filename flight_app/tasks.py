"""Celery tasks:
    - weather task. get data from weather api for number of HOURS and store it in DB
    - flight task. get data from airport Schiphol api and store it in DB
    - ElasticSearch task. get data from DB and store (or update) it in ElasticSearch docs
    - Chain task. create queue of above tasks
    """
import datetime
from celery import shared_task, chain

from flight_app.service_flights import FlightService
from flight_app.service_weather import WeatherService
from flight_app.service_es_doc import create_es_doc

# get data for 14 days
DAYS_AGO = 9
DAYS_AHEAD = 9
PERIOD = DAYS_AGO + DAYS_AHEAD + 1

# get forecast for 7 days (equal 168 hours)
HOURS = 168


def start_day() -> datetime.date:
    """Function count date of first day of period we want to store data.
     It equals today - period days ago
        :return datetime.date"""
    today = datetime.date.today()
    difference_between_days = datetime.timedelta(days=DAYS_AGO)
    return today - difference_between_days


@shared_task
def parse_weather_task():
    """Weather task
    Celery task for running service_weather.py for some days (days count in hours, look above HOURS)
    Task starts from chain (look chain_task())"""
    parse_weather = WeatherService(HOURS)
    parse_weather.parse()
    return True


@shared_task
def parse_flights_task():
    """Flight task
    Celery task for running service_flights.py for some days (look above 'PERIOD')
    Task starts from chain (look chain_task())"""
    current_day = start_day()
    for _ in range(PERIOD):
        parse_flights = FlightService(current_day)
        parse_flights.parse()
        current_day += datetime.timedelta(days=1)
    return True


@shared_task
def add_docs_into_es():
    """ElasticSearch task
    Celery task for running service_es_doc.py for some days (look above 'PERIOD')
    Task starts from chain (look chain_task())"""
    current_day = start_day()
    for _ in range(PERIOD):
        create_es_doc(current_day)
        current_day += datetime.timedelta(days=1)
    return True


@shared_task
def chain_task():
    """Chain task
    Create queue of tasks, each chain's task - independent task (<task_name>.si() - immutable signatures)
    Task starts by schedule (look setting.py CELERY_BEAT_SCHEDULE)"""
    res = chain(parse_weather_task.si(), parse_flights_task.si(), add_docs_into_es.si())()
    res.get()
