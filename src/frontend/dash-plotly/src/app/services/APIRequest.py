import requests


class APIRequest:
    def __init__(self):
        self.api_url = "http://127.0.0.1:5000"

    def get(self, route):
        response = requests.get(self.api_url + route)
        if response.status_code == 200:
            return response.json()
        return None
