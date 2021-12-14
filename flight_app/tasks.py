from datetime import datetime
from celery import shared_task

from flight_app.models import Flight, Airport

# from celery


@shared_task
def parse_flights_task():
    airport = Airport(name='DOM').save()
    print(datetime.now())
    print("add airport", datetime.now())
    return Airport.objects.count()
