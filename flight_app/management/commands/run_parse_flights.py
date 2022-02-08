"""Create django custom command, for run:
    'python manage.py run_parse_flights [date] [-p --period]'
    """
from datetime import datetime
from django.core.management.base import BaseCommand

from flight_app.service_flights import FlightService


class Command(BaseCommand):
    """Create django custom command, for run:
    'python manage.py run_parse_flights [date] [-p --period]'
    Date must be yyyy-MM-dd format, for default today
    Period must contains two dates in yyyy-MM-dd format"""
    help = 'Run parse_flights_task'

    def add_arguments(self, parser):
        """Create 2 command arguments
            :argument date: str, must be yyyy-MM-dd format, for default today
            :argument -p or --period: list[str, str], dates must be yyyy-MM-dd format"""
        parser.add_argument('date', type=str, nargs='?', default=None,
                            help='date must be in yyyy-MM-dd format, by default - today')
        parser.add_argument('-p', '--period', nargs=2, type=str,
                            help='must be 2 dates. date must be in yyyy-MM-dd format')

    def handle(self, *args, **options):
        """Create object of ParseFlights and call parse method
            :raise ValueError in case input date has wrong format"""
        period = options['period']
        if period:
            # raise ValueError in case date has wrong format
            datetime.strptime(period[0], '%Y-%m-%d')
            datetime.strptime(period[1], '%Y-%m-%d')

            parse_flights = FlightService(None, period[0], period[1])
            parse_flights.parse()
        else:
            if options['date']:
                # raise ValueError in case date has wrong format
                datetime.strptime(options['date'], '%Y-%m-%d')

            parse_flights = FlightService(options['date'])
            parse_flights.parse()
