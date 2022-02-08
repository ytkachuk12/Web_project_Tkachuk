"""Get a data from the DB for current date and add it into ElasticSearch index"""
from django.forms.models import model_to_dict
from elasticsearch import Elasticsearch

from django.conf import settings
from flight_app.models import Flight, FlightAirport


def create_es_doc(date):
    """Get a data from the DB for current date and add it into ElasticSearch index
        :param date: format date"""

    # crete ElasticSearch obj
    es = Elasticsearch(hosts=settings.ELASTIC_HOST)

    # get the data from DB for current date
    flights = Flight.objects.filter(schedule_date_time__date=date)
    for flight in flights:
        # convert Flight's instance into dictionary
        flight_model = model_to_dict(flight)
        # assign airline field to converted into dictionary one_to_many relation with Airline instance
        flight_model['airline'] = model_to_dict(flight.airline)
        # assign aircraft field to converted into dictionary one_to_many relation with Aircraft instance
        flight_model['aircraft'] = model_to_dict(flight.aircraft)
        # assign status field to converted into list[ of dictionary] many_to_many relation with Status instance
        flight_model['status'] = [model_to_dict(status, fields='name') for status in flight_model['status']]
        # assign airport field to converted into list[ of dictionary] many_to_many relation with Airport.name field
        # and FlightAirport from_to_marker field
        temp = []
        for flight_airport in flight_model['airport']:
            # get from_to_marker's field from FlightAirport (receive it in dict type)
            all_airport_data = FlightAirport.objects.filter(flight=flight.id, airport=flight_airport.id)\
                .values("from_to_marker")[0]
            # add the field "name" to dict with from_to_marker's field
            all_airport_data['name'] = flight_airport.name
            temp.append(all_airport_data)
        flight_model['airport'] = temp

        # add or update doc to ElasticSearch
        es.index(index=settings.ELASTIC_INDEX_NAME, doc_type="_doc", id=flight.id, body=flight_model)
