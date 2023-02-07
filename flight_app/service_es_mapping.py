"""Service for crete ElasticSearch index with mapping."""

from elasticsearch import Elasticsearch

from django.conf import settings


def create_es_mapping():
    """Create ES index, with name - ELASTIC_INDEX_NAME, hosts - ELASTIC_HOST(look settings.py)
         and body - index_mapping"""

    # crete ElasticSearch obj
    es = Elasticsearch(hosts=settings.ELASTIC_HOST)

    index_mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "dynamic": "false",  # maybe strict
            "properties": {
                "name": {"type": "text"},
                "last_update": {"type": "date"},
                "schedule_date_time": {"type": "date"},
                "actual_landing_time": {"type": "date", "null_value": "NULL"},
                "actual_off_time": {"type": "date", "null_value": "NULL"},
                "expected_boarding_time": {"type": "date", "null_value": "NULL"},
                "estimate_landing_time": {"type": "date", "null_value": "NULL"},
                "airline": {
                    "properties": {
                        "code": {"type": "integer"},
                        "ICAO": {"type": "keyword"},
                        "IATA": {"type": "keyword"}
                    }
                },
                "aircraft": {
                    "properties": {
                        "type": {"type": "keyword"},
                        "registration": {"type": "keyword"}
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
                        "name": {"type": "keyword"},
                        "from_to_marker": {"type": "keyword"}
                    }
                }
            }
        }
    }

    # create index
    es.indices.create(index=settings.ELASTIC_INDEX_NAME, ignore=400, body=index_mapping)
