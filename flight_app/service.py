"""In progress"""

import os
from typing import Optional
import requests

from flight_app.serializers import FlightSerializer, AircraftSerializer, AirlineSerializer, AirportSerializer


class FlightService:
    """Service - take data from API, parse it and save into DB"""
    URL = 'https://api.schiphol.nl/public-flights/flights'
    APP_ID = os.environ.get("API_ID")
    APP_KEY = os.environ.get("API_KEY")
    HEADERS = {
        "accept": "application/json",
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "resourceversion": "v4"
    }

    def __init__(self, date: Optional[str], from_date: str = None, to_date: str = None):
        self.PAYLOAD = {
            "scheduleDate": date,
            "fromScheduleDate": from_date,
            "toScheduleDate": to_date,
        }

    def parse(self):
        """In progress
        Make request to API
        Serialize response"""
        request_to_api = requests.Session()
        response_from_api = request_to_api.get(url=self.URL, headers=self.HEADERS, params=self.PAYLOAD)
        list_flights = response_from_api.json()
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
