"""WeatherService - request data from weather API - https://api.weatherbit.io/v2.0/forecast/hourly,
    parse data (serializers.py) """
import os
import requests

from django.conf import settings
from flight_app.serializers import WeatherSerializer


class WeatherService:
    """WeatherService - take data from weather API, parse it and save into DB
        URL: API url
        ACCESS_KEY: API user's key(set in .env file)"""
    URL = settings.URL_WEATHER
    ACCESS_KEY = os.environ.get("WEATHER_KEY")

    def __init__(self, hours):
        self.PAYLOAD = {
            "key": self.ACCESS_KEY,
            "city": "Amsterdam",
            "country": "NL",
            "hours": hours
        }

    def parse(self):
        """Make request to API
        Serialize response"""
        request_to_api = requests.Session()
        response_from_api = request_to_api.get(url=self.URL, params=self.PAYLOAD)
        weather = response_from_api.json()
        # parse forecast hourly weather
        for hourly_weather in weather['data']:
            deserialized_weather = WeatherSerializer(data=hourly_weather)

            # save data into DB if data is valid
            if deserialized_weather.is_valid():
                deserialized_weather.save()
