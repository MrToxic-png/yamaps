from typing import Iterable

import requests

from config import STATIC_MAPS_API_KEY
from yandex_maps_api.pointer import Pointer


def get_static_maps_image(longitude: float,
                          latitude: float,
                          zoom: int,
                          theme: str,
                          pointers: Iterable[Pointer] | None = None) -> bytes | None:
    server = 'https://static-maps.yandex.ru/v1'

    params = {'apikey': STATIC_MAPS_API_KEY,
              'll': f'{longitude},{latitude}',
              'z': str(zoom),
              'theme': theme}

    if pointers is not None:
        params['pt'] = '~'.join(map(str, pointers))

    response = requests.get(server, params=params)
    if not response:
        return None
    return response.content
