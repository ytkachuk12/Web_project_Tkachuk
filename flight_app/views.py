"""Flight_app views:
    - for route /flights/
    - for route /flight/"""

from django.http import HttpResponse
from rest_framework import generics, mixins

from flight_app.models import Flight, Weather
from flight_app.serializers import ResponseFlightSerializer, WeatherSerializer


def index(request):
    return HttpResponse("Hello")


class FlightListView(generics.ListAPIView):
    """View for route /flights/"""
    serializer_class = ResponseFlightSerializer

    def get_queryset(self):
        """Filter queryset by:
            - without filter(all flights)
            - by date
            - by period"""
        queryset = Flight.objects.all().order_by('schedule_date_time')
        date = self.request.query_params.get('date', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if date:
            queryset = queryset.filter(schedule_date_time__date=date).order_by('schedule_date_time')
        elif start_date and end_date:
            queryset = queryset.filter(schedule_date_time__range=[start_date, end_date]).order_by('schedule_date_time')

        return queryset


class FlightView(generics.ListAPIView):
    """View for route /flight/"""
    serializer_class_flight = ResponseFlightSerializer
    serializer_class_weather = WeatherSerializer

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
        flight_id = self.request.query_params.get('id', None)

        # get queryset flight schedule date and time
        flight = Flight.objects.filter(id=flight_id).values_list('schedule_date_time', flat=True)
        # for filter weather - round datetime to hour (replace microsecond=0, second=0 and minute=0)
        return Weather.objects.filter(datetime=flight[0].replace(microsecond=0, second=0, minute=0))

    def list(self, request, *args, **kwargs):
        """get data from ResponseFlightSerializer and WeatherSerializer"""
        flight = self.serializer_class_flight(self.get_queryset_flight(), many=True)
        weather = self.serializer_class_weather(self.get_queryset_weather(), many=True)
        return mixins.Response({"flight": flight.data, "weather": weather.data})
