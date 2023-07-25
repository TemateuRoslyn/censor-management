import os
import requests

API_ADDR = os.getenv("API_ADDR")


def get_request(route: str):
    """Fonction qui doit lancer les requêtes en GET a l'API"""
    response = requests.get(API_ADDR + route)
    if response.status_code == 200:
        return response.json()
    else:
        return None
