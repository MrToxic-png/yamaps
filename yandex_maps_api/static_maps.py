from config import STATIC_MAPS_API_KEY
import requests


def get_static_maps_image() -> bytes | None:
    server = ''

    params = {'apikey': STATIC_MAPS_API_KEY}

    response = requests.get(server, params=params)
    if not response:
        return None
    return response.content
