"""Create django custom command, for crete ElasticSearch index with mappind.
    Mapping by default create during migrate
    """
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch

from django.conf import settings


class Command(BaseCommand):
    """Create django custom command, for create ElasticSearch index with mapping
    """
    help = 'Run es'

    def handle(self, *args, **options):

        es = Elasticsearch(hosts=settings.ELASTIC_HOST)

        index_mapping = {
            "settings": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            },
            "mappings": {
                "dynamic": "false",  # maybe strict
                "properties": {
                    "name": {"type": "text"},
                    "last_update": {"type": "date", "format": "yyyy-MM-dd"},
                    "schedule_date_time": {"type": "date", "format": "yyyy-MM-dd"},
                    "actual_landing_time": {"type": "date", "format": "yyyy-MM-dd", "null_value": "NULL"},
                    "actual_off_time": {"type": "date", "format": "yyyy-MM-dd", "null_value": "NULL"},
                    "expected_boarding_time": {"type": "date", "format": "yyyy-MM-dd", "null_value": "NULL"},
                    "estimate_landing_time": {"type": "date", "format": "yyyy-MM-dd", "null_value": "NULL"},
                    "airline": {
                        "properties": {
                            "code": {"type": "integer"},
                            "ICAO": {"type": "text"},
                            "IATA": {"type": "text"}
                        }
                    },
                    "aircraft": {
                        "properties": {
                            "type": {"type": "text"},
                            "registration": {"type": "text"}
                        }
                    },
                    "status": {
                        "type": "nested",
                        "properties": {
                            "name": {"type": "text"}
                        }
                    },
                    "airport": {
                        "type": "nested",
                        "properties": {
                            "name": {"type": "text"},
                            "from_to_marker": {"type": "text"}
                        }
                    }
                }
            }
        }

        # create index
        es.indices.create(index="flights", ignore=400, body=index_mapping)