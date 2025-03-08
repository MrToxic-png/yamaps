import requests

from config import STATIC_MAPS_API_KEY


def get_static_maps_image(longitude: float, latitude: float, zoom: int) -> bytes | None:
    server = 'https://static-maps.yandex.ru/v1'

    params = {'apikey': STATIC_MAPS_API_KEY,
              'll': f'{longitude},{latitude}',
              'z': str(zoom)}

    response = requests.get(server, params=params)
    if not response:
        return None
    return response.content
