import requests

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
URL = 'https://api.schiphol.nl/public-flights/flights'
HEADERS = {"Accept": "application/json", "app_id": "2bf2e7d5", "app_key": "a90c8fe47ea1f6d519d9887f8e05d6ce",
           "ResourceVersion": "v4"}
PAYLOAD = {"includedelays": "false" , "page": 0, "sort": "%2BscheduleTime", "scheduleDate": "2021-12-07"}


def index(request):

    return HttpResponse("Hello")