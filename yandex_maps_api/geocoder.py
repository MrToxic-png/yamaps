import requests

from config import GEOCODER_API_KEY
from typing import Self


class Geocoder:
    def __init__(self, toponym: str):
        geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
        geocoder_params = {
            'apikey': GEOCODER_API_KEY,
            'geocode': toponym,
            'format': 'json'}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            raise requests.exceptions.RequestException('Error when handling the request')

        self._full_json = response.json()
        self._name = toponym
        try:
            self._get_first_geo_object()
        except (KeyError, IndexError):
            raise ValueError('GeoObject not found')

    @classmethod
    def from_cords(cls, longitude: float, latitude: float) -> Self:
        geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
        geocoder_params = {
            'apikey': GEOCODER_API_KEY,
            'geocode': ', '.join(map(str, (longitude, latitude))),
            'format': 'json'}

        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            raise requests.exceptions.RequestException('Error when handling the request')

        response_data = response.json()

        best_geo_object = response_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        full_address = best_geo_object['metaDataProperty']['GeocoderMetaData']['text']

        return cls(full_address)

    def _get_first_geo_object(self):
        return self._full_json['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']

    @property
    def point(self) -> tuple[float, float]:
        geo_object_point: list[str, str] = self._get_first_geo_object()['Point']['pos'].split()
        longitude, latitude = float(geo_object_point[0]), float(geo_object_point[1])
        return longitude, latitude

    @property
    def longitude(self) -> float:
        return self.point[0]

    @property
    def latitude(self) -> float:
        return self.point[1]

    @property
    def full_address(self) -> str:
        return self._get_first_geo_object()['metaDataProperty']['GeocoderMetaData']['text']

    @property
    def postal_code(self) -> str | None:
        return self._get_first_geo_object()['metaDataProperty']['GeocoderMetaData']['Address'].get('postal_code')
