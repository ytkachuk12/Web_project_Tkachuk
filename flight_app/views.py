"""Flight_app views:
    - for route /flights/
    - for route /flight/
    - for route /search/"""

from django.http import HttpResponse
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from flight_app.models import Flight, Weather
from flight_app.serializers import ResponseFlightSerializer, WeatherSerializer, RequestSearchSerializer
from flight_app.service_es_search import SearchService


def index(request):
    return HttpResponse("Hello")


class FlightListView(generics.ListAPIView):
    """View for route /flights/"""
    serializer_class = ResponseFlightSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset by:
            - without filter(all flights)
            - by date
            - by period"""
        queryset = Flight.objects.all().order_by('schedule_date_time')
        date = self.request.query_params.get('date')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if date:
            queryset = queryset.filter(schedule_date_time__date=date).order_by('schedule_date_time')
        elif start_date and end_date:
            queryset = queryset.filter(schedule_date_time__range=[start_date, end_date]).order_by('schedule_date_time')

        return queryset


class FlightView(generics.ListAPIView):
    """View for route /flight/"""
    serializer_class_flight = ResponseFlightSerializer
    serializer_class_weather = WeatherSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset_flight(self):
        """Filter Flight queryset by:
            - by name(can be not unique flight)
            - by id(unique flight)"""
        # get parameters from request
        flight_id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')
        # filter by fight name or by id
        if name:
            queryset = Flight.objects.filter(name=name)
        else:
            queryset = Flight.objects.filter(id=flight_id)
        return queryset

    def get_queryset_weather(self):
        """Filter Weather queryset by:
            - by current flight datetime where time round to hour(replace microsecond=0, second=0 and minute=0)"""
        # get parameters from request
        flight_id = self.request.query_params.get('id')

        # get queryset flight schedule date and time
        flight = Flight.objects.filter(id=flight_id).values_list('schedule_date_time', flat=True)
        # for filter weather - round datetime to hour (replace microsecond=0, second=0 and minute=0)
        return Weather.objects.filter(datetime=flight[0].replace(microsecond=0, second=0, minute=0))

    def list(self, request, *args, **kwargs):
        """get data from ResponseFlightSerializer and WeatherSerializer"""
        flight = self.serializer_class_flight(self.get_queryset_flight(), many=True)
        weather = self.serializer_class_weather(self.get_queryset_weather(), many=True)
        return mixins.Response({"flight": flight.data, "weather": weather.data})


class SearchView(APIView):
    """View for route /search/, method GET"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        """Method GET.
        get data from request, serialize it and call SearchService(look service_es_search.py)"""
        # get all request's parameters
        data = self.request.query_params
        # pass it into serializer
        serializer = RequestSearchSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            search_service = SearchService(**serializer.data)
            response = search_service.search()
        return Response(response)
