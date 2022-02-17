"""AirportService - request data from Schiphol airport API - https://api.schiphol.nl/public-flights/destinations/{iata}
    parse data (serializers.py) """

import os
import requests

from django.conf import settings
from flight_app.models import Airport
from flight_app.serializers import AirportDescriptionSerializer


class AirportService:
    """Service - take data from API, parse it and save into DB
        URL: API url
        APP_ID: API user's id(set in .env file)
        APP_KEY: API user's key(set in .env file)

    Service take data from api:
        - per day(must be in ISO 8601 format: '2022-01-01')
        - per period: from_date, to_date(api returns data fo 2 days period only)"""
    URL = settings.URL_AIRPORTS
    APP_ID = os.environ.get("API_ID")
    APP_KEY = os.environ.get("API_KEY")
    HEADERS = {
        "accept": "application/json",
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "resourceversion": "v4"
    }

    def get_all_airports(self):
        """Get all airports
        Create correct url endpoint(add IATA code into request endpoint)
        Call parser"""

        airports = Airport.objects.all()
        for airport in airports:

            url_with_IATA_code = self.URL + airport.name

            self.parse(airport, url_with_IATA_code)

    def parse(self, airport, url_with_IATA_code):
        """Make request to API
        Serialize response, update Airport's public_name, city, country"""
        # api request
        request_to_api = requests.Session()
        response_from_api = request_to_api.get(url=url_with_IATA_code, headers=self.HEADERS)
        airport_data = response_from_api.json()

        # parse airport public name, city, country
        # create instances of serializers
        deserialized_airport = AirportDescriptionSerializer(data=airport_data)

        # update data into DB if data is valid
        if deserialized_airport.is_valid():
            deserialized_airport.update(airport, validated_data=deserialized_airport.validated_data)
