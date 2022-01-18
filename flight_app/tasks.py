import datetime
from celery import shared_task

from flight_app.service import FlightService

# from celery

DAYS_AGO = 7
DAYS_AHEAD = 7
period = DAYS_AGO + DAYS_AHEAD + 1


# START_DAY = '2021-12-10'  # os.environ.get('START_DAY')
# PERIOD = 7  # os.environ.get('PERIOD')

def start_day() -> datetime.date:
    """Function count date of first day of period we want to store data.
     It equal today - period days ago
        :return datetime.date"""
    today = datetime.date.today()
    difference_between_days = datetime.timedelta(days=DAYS_AGO)
    return today - difference_between_days


@shared_task
def parse_flights_task():
    current_day = start_day()
    print("START TASK")
    for _ in range(period):
        parse_flights = FlightService(current_day)
        parse_flights.parse()
        current_day += datetime.timedelta(days=1)
    return True
