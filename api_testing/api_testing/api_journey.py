import requests
import json
from api_testing.core import Core


class Api_Journey():
    def __init__(self):
        pass

    def orders(self, endpoint=None, payloads=None):
        return requests.post(endpoint, json=payloads)

    def fetch_data_endpoint(self, endpoint=None):
        return requests.get(endpoint)

    def take_complete_cancel_endpoint(self, endpoint=None):
        return requests.put(endpoint)
