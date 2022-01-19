"""flight_app URL Configuration

There are 3 path:
    - index (empty)
    - flights list of flights (all, per day, per period)
    - flight info about current flight and TODO: weather"""
from django.urls import path

from . import views
from flight_app.views import FlightListView, FlightView

app_name = 'flight_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('flights/', FlightListView.as_view(), name='flights'),
    path('flight/', FlightView.as_view(), name='flight'),
]
