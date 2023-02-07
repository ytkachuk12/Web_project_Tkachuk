"""Create django custom command, for run:
    'python manage.py create_es_docs [date]'
    """
from django.core.management.base import BaseCommand
from datetime import datetime

from flight_app.service_es_doc import create_es_doc


class Command(BaseCommand):
    """Create django custom command, for create or update ElasticSearch docs for current date.
        Name - ELASTIC_INDEX_NAME, hosts - ELASTIC_HOST(look settings.py)
        and body - index_mapping(for code look create_es_docs.py)"""
    help = 'The command run creation or updating ElasticSearch docs'

    def add_arguments(self, parser):
        """Create  command argument
            :argument date: str, must be yyyy-MM-dd format, for default today"""
        parser.add_argument('date', type=str, nargs='?', default=None,
                            help='date must be in yyyy-MM-dd format, by default - today')

    def handle(self, *args, **options):
        """Add docs into ElasticSearch
            :raise ValueError in case input date has wrong format"""
        if options['date']:
            # raise ValueError in case date has wrong format
            date = datetime.strptime(options['date'], '%Y-%m-%d')
        else:
            date = datetime.today()
        create_es_doc(date)
