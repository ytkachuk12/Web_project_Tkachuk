"""In progress"""

import os
from typing import Optional

import requests


class FlightService:
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
        # add with func
        request_to_api = requests.Session()
        response_from_api = request_to_api.get(url=self.URL, headers=self.HEADERS, params=self.PAYLOAD)
        list_flights = response_from_api.json()
        for flight in list_flights['flights']:
            print(flight)
            pass
