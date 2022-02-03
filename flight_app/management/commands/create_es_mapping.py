"""Create django custom command, for crete ElasticSearch index with mapping.
    for run: 'python manage.py es_index_mapping' without arguments"""
from django.core.management.base import BaseCommand

from flight_app.service_es_mapping import create_es_mapping


class Command(BaseCommand):
    """Create django custom command, for create ElasticSearch index with mapping
        Name - ELASTIC_INDEX_NAME, hosts - ELASTIC_HOST(look settings.py)
        and body - index_mapping(for code look create_es_mapping.py)"""
    help = 'Run es'

    def handle(self, *args, **options):
        """For code - look create_es_mapping.py file"""
        create_es_mapping()
