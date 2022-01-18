"""Flight_app views:
    - for route /flights/
    - for route /flight/"""

from django.http import HttpResponse
from rest_framework import generics, filters

from flight_app.models import Flight
from flight_app.serializers import ResponseFlightSerializer


def index(request):
    return HttpResponse("Hello")


class FlightListView(generics.ListAPIView):
    """View for route /flights/"""
    serializer_class = ResponseFlightSerializer

    def get_queryset(self):
        """Filter queryset by:
            - without filter(all flights
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
    """View for route /flights/
    TODO add weather"""
    serializer_class = ResponseFlightSerializer

    def get_queryset(self):
        """Filter queryset by:
            - by name(can be not unique flight)
            - by id(unique flight)"""
        flight_id = self.request.query_params.get('id', None)
        name = self.request.query_params.get('name', None)
        if name:
            queryset = Flight.objects.filter(name=name)
        else:
            queryset = Flight.objects.filter(id=flight_id)
        return queryset
