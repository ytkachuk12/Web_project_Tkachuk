"""Create django custom command, for ElasticSearch _search method.
    for run:
    'python manage.py es_search [-n --name] [-d --date] [-p --period]
                        [--code] [--ICAO] [--IATA] [--status] [--airport]
                        [--connected] [--pagination]':
    """
from datetime import datetime
from django.core.management.base import BaseCommand

from flight_app.service_es_search import SearchService


class Command(BaseCommand):
    """Create django custom command, for ElasticSearch _search method
    for run: 'python manage.py es_search [with or without(for all docs) param]'
        [-n --name]: str, filter by flight name
        [-d --date]: str, filter by flight date, date must be in yyyy-MM-dd format
        [--start_date]: str, filter by flight period, date must be in yyyy-MM-dd format
        [--last_date]: str, filter by flight period, date must be in yyyy-MM-dd format
        [--code]: int, filter by airline code
        [--ICAO]: str, filter by airline ICAO abbr
        [--IATA]: str, filter by airline IATA abbr
        [--status]: str, filter by flight status abbr
        [--airport]: str, filter by airport abbr
        [--connected]: str, filter by connected or not flights (choices 'y' or 'n')
        [--pagination]: int, quantity of returning docs, by default 10
        """
    help = 'the command run ElasticSearch _search method'

    def add_arguments(self, parser):
        """Create command arguments
        :argument name: str, filter by flight name
        :argument date: str, filter by flight date, date must be in yyyy-MM-dd format
        :argument start_date: str, filter by flight period, date must be in yyyy-MM-dd format
        :argument last_date: str, filter by flight period, date must be in yyyy-MM-dd format
        :argument code: int, filter by airline code
        :argument ICAO: str, filter by airline ICAO abbr
        :argument IATA: str, filter by airline IATA abbr
        :argument status: str, filter by flight status abbr
        :argument airport: str, filter by airport abbr
        :argument connected: str, filter by connected or not connected flights, choices 'y' or  'n'
        :argument pagination: int, set quantity of returning docs, by default 10
        """
        parser.add_argument('-n', '--name', type=str, help='filter by flight name')

        parser.add_argument('-d', '--date', type=str, help='date must be in yyyy-MM-dd format')
        parser.add_argument('--start_date', type=str, help="period's start date, date must be in yyyy-MM-dd format")
        parser.add_argument('--last_date', type=str, help="period's last date, date must be in yyyy-MM-dd format")

        parser.add_argument('--code', type=int, help='filter by airline code')
        parser.add_argument('--ICAO', type=str, help='filter by airline ICAO abbr')
        parser.add_argument('--IATA', type=str, help='filter by airline IATA abbr')

        parser.add_argument('--status', type=str, help='filter by status abbr')

        parser.add_argument('--airport', type=str, help='filter by airport abbr')
        parser.add_argument('--connected', choices=['y', 'n'], help='filter by connected or not connected flights')

        parser.add_argument('--size', type=int, default=10, help='number of returning es docs per page')
        parser.add_argument('--page', type=int, default=0, help='number of returning page')

    def handle(self, *args, **options):
        """Create object of SearchService and call .search method
            :raise ValueError in case input dates have wrong format"""
        if options['date']:
            # raise ValueError in case date has wrong format
            datetime.strptime(options['date'], '%Y-%m-%d')
        if options['start_date'] or options['last_date']:
            # raise ValueError in case dates have wrong format
            datetime.strptime(options['start_date'], '%Y-%m-%d')
            datetime.strptime(options['last_date'], '%Y-%m-%d')

        search_service = SearchService(**options)
        res = search_service.search()
        self.print_out(res)

    @staticmethod
    def print_out(res):
        for flight in res[1]:
            print(flight)
            print()
        print(res[0])  # print of total quantity matched docs
