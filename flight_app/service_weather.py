import os
import requests

from flight_app.serializers import WeatherSerializer


class WeatherService:
    """WeatherService - take data from weather API and parse it"""
    URL = 'https://api.weatherbit.io/v2.0/forecast/hourly'
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
