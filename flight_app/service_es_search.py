"""Search data in ElasticSearch index 'flights'"""
from elasticsearch import Elasticsearch

from django.conf import settings

# crete ElasticSearch obj
es = Elasticsearch(hosts=settings.ELASTIC_HOST)


class SearchService:
    """SearchService - retrieve data from ES
    Search by flight name(or part or flight name)
    Filter by:
        - schedule date
        - schedule period(start date, stop date)
        - airline code or ICAO abbr or IATA abbr
        - status of flight
        - airport abbr
        - connected or not connected flight"""

    def __init__(self, **kwargs):
        """ arguments are -
        :param name Optional[str], search by flight name or part of it
        :param date Optional[date], filter by current date
        :param period Optional[list(date, date)], filter by period between first date and second date(included)
        :param airline_code Optional[int], filter by airline code
        :param airline_ICAO Optional[str], filter by airline ICAO abbr
        :param airline_IATA Optional[str], filter by airline IATA abbr
        :param status Optional[str], filter by airline IATA abbr
        :param airport Optional[str], filter by airport abbr
        :param connected_flight Optional['y' or 'n'], filter by availability connected airport
        from_to_marker='TRAN' for connected flight and have no transition airport for not connected flight
        :param size int, pagination size(quantity of printing out results), by default 10
        :param _from int, number of first returning doc(depends on number of doc's per page and page number)
        :param query_body - structure of search query, include
            'must': search param, and 'filter': filter param"""
        self.name = kwargs['name']

        self.date = kwargs['date']
        self.period = [kwargs['start_date'], kwargs['last_date']]

        self.airline_code = kwargs['code']
        self.airline_ICAO = kwargs['ICAO']
        self.airline_IATA = kwargs['IATA']

        self.status = kwargs['status']

        self.airport = kwargs['airport']
        self.connected_flight = kwargs['connected']

        self.size = kwargs['size']
        # count number of first returning doc(depends on number of doc's per page and page number)
        self._from = kwargs['page'] * self.size + 1

        self.query_body = {
            "from": self._from,
            "size": self.size,
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            }
        }

    def build_query(self):
        """Add into query search and filters param
            'must': [list] - key for search
            'filter': [list] - key for diff filters"""
        # add into 'must' dict key - search by flight name
        if self.name:
            self.query_body['query']['bool']["must"].append(
                {"query_string": {"query": "*" + self.name + "*", "default_field": "name"}})

        # add into 'filter' key - or date or period filter
        if self.date:
            self.query_body['query']['bool']["filter"].append(
                {"range": {"schedule_date_time": {"gte": self.date, "lte": self.date}}}
            )
        elif self.period[0] and self.period[1]:
            self.query_body['query']['bool']["filter"].append(
                {"range": {"schedule_date_time": {"gte": self.period[0], "lte": self.period[1]}}}
            )

        # add into 'filer' key - or airline code or ICAO or IATA filter
        if self.airline_code:
            self.query_body['query']['bool']["filter"].append(
                {"term": {"airline.code": self.airline_code}})
        elif self.airline_ICAO:
            self.query_body['query']['bool']["filter"].append(
                {"term": {"airline.ICAO": self.airline_ICAO.lower()}})
        elif self.airline_IATA:
            self.query_body['query']['bool']["filter"].append(
                {"term": {"airline.IATA": self.airline_IATA.lower()}})

        # add into 'filter' key - status filter
        if self.status:
            self.query_body['query']['bool']["filter"].append(
                {"nested": {
                    "path": "status",
                    "query": {
                        "bool":
                            {"filter": [{"term": {"status.name": self.status.lower()}}]}
                    }
                }})

        # add into 'filter' key - airport name filter
        if self.airport:
            self.query_body['query']['bool']["filter"].append(
                {"nested": {
                    "path": "airport",
                    "query": {
                        "bool":
                            {"filter": [{"term": {"airport.name": self.airport.lower()}}]}
                    }
                }})

        # add into 'filter' key - connected flight or not connected flight filter
        if self.connected_flight == 'y':
            self.query_body['query']['bool']["filter"].append(
                {"nested": {
                    "path": "airport",
                    "query": {
                        "bool":
                            {"filter": [{"term": {"airport.from_to_marker": "tran"}}]}
                    }
                }})
        elif self.connected_flight == 'n':
            self.query_body['query']['bool']["filter"].append(
                {"nested": {
                    "path": "airport",
                    "query": {
                        "bool":
                            {"must_not": [{"term": {"airport.from_to_marker": "tran"}}]}
                    }
                }})

    def search(self):
        """ES search
        call build_query than make search by this query and print_out results"""
        self.build_query()
        res = es.search(index=settings.ELASTIC_INDEX_NAME, body=self.query_body)
        return res['hits']['total'], res['hits']['hits']
