import requests

from .geocoder import Geocoder
from .pointer import Pointer
from .static_maps import get_static_maps_image

START_POINT = (37.617698, 55.755864)
START_ZOOM = 10
BASE_OFFSET = 64

THEME_SWITCH_DICT = {'light': 'dark', 'dark': 'light'}


class PointMap:
    def __init__(self):
        self._longitude, self._latitude = START_POINT
        self._zoom = START_ZOOM
        self._theme = 'light'
        self._geocoder: Geocoder | None = None

    def get_image(self) -> bytes:
        if self._geocoder:
            pointer = Pointer(self._geocoder.longitude, self._geocoder.latitude, other_info='org')
            return get_static_maps_image(self._longitude, self._latitude, self._zoom, self._theme, pointers=(pointer,))
        else:
            return get_static_maps_image(self._longitude, self._latitude, self._zoom, self._theme)

    def decrease_zoom(self):
        self._zoom = max(self._zoom - 1, 0)

    def increase_zoom(self):
        self._zoom = min((self._zoom + 1, 21))

    def move_up(self):
        self._latitude += BASE_OFFSET / 2 ** self._zoom
        if self._latitude > 90:
            self._latitude = 90

    def move_down(self):
        self._latitude -= BASE_OFFSET / 2 ** self._zoom
        if self._latitude < -90:
            self._latitude = -90

    def move_right(self):
        self._longitude += BASE_OFFSET / 2 ** self._zoom
        if self._longitude > 180:
            self._longitude -= 360

    def move_left(self):
        self._longitude -= BASE_OFFSET / 2 ** self._zoom
        if self._longitude < -180:
            self._longitude += 360

    def switch_theme(self):
        self._theme = THEME_SWITCH_DICT.get(self._theme)

    def find_toponym(self, toponym: str):
        try:
            self._geocoder = Geocoder(toponym)
            self._longitude, self._latitude = self._geocoder.point
        except (ValueError, requests.exceptions.RequestException):
            return

    def clear_geocoder(self):
        self._geocoder = None

    def get_geocoder_full_address(self, postal_code: bool = False) -> str | None:
        if self._geocoder is None:
            return None
        if postal_code and self._geocoder.postal_code:
            return f'{self._geocoder.full_address}\nПочтовый индекс: {self._geocoder.postal_code}'

        return self._geocoder.full_address
