"""Create django custom command.
    Get airport's full public name, city, country
    for run: 'python manage.py get_airport' without arguments"""
from django.core.management.base import BaseCommand

from flight_app.service_airports import AirportService


class Command(BaseCommand):
    """Create django custom command.
        Get airport's full public name, city, country
        """
    help = 'the command run get_airport'

    def handle(self, *args, **options):
        """For code - look service_airport.py file"""
        airport_service = AirportService()
        airport_service.get_all_airports()
