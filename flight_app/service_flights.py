"""FlightService - request data from Schiphol airport API - https://api.schiphol.nl/public-flights/flights
    parse data (serializers.py) """

import os
from typing import Optional
import requests

from django.conf import settings
from flight_app.serializers import FlightSerializer, AircraftSerializer, AirlineSerializer, AirportSerializer


class FlightService:
    """Service - take data from API, parse it and save into DB
        URL: API url
        APP_ID: API user's id(set in .env file)
        APP_KEY: API user's key(set in .env file)

    Service take data from api:
        - per day(must be in ISO 8601 format: '2022-01-01')
        - per period: from_date, to_date(api returns data fo 2 days period only)"""
    URL = settings.URL_FLIGHTS
    APP_ID = os.environ.get("API_ID")
    APP_KEY = os.environ.get("API_KEY")
    HEADERS = {
        "accept": "application/json",
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "resourceversion": "v4"
    }

    def __init__(self, date: Optional[str], from_date: str = None, to_date: str = None):
        """day: load flights per current day(must be in ISO 8601 format: '2022-01-01')
        from_date, to_date: load flights per period(api returns data fo 2 days period only)"""
        self.PAYLOAD = {
            "scheduleDate": date,
            "fromScheduleDate": from_date,
            "toScheduleDate": to_date,
        }

    def parse(self):
        """Make request to API
        Serialize response"""
        request_to_api = requests.Session()
        response_from_api = request_to_api.get(url=self.URL, headers=self.HEADERS, params=self.PAYLOAD)
        list_flights = response_from_api.json()
        # parse flights
        for flight in list_flights['flights']:
            # create instances of serializers
            deserialized_aircraft = AircraftSerializer(data=flight)
            deserialized_airline = AirlineSerializer(data=flight)
            deserialized_flight = FlightSerializer(data=flight)
            deserialized_airport = AirportSerializer(data=flight['route']['destinations'])

            # save data into DB if data is valid
            if deserialized_airport.is_valid():
                deserialized_airport.save()

            if deserialized_aircraft.is_valid():
                deserialized_aircraft.save()

            if deserialized_airline.is_valid():
                deserialized_airline.save()

            if deserialized_flight.is_valid():
                deserialized_flight.save()
