import math

import geopy.distance
import pyproj
import requests

from .geocoder import Geocoder
from .pointer import Pointer
from .static_maps import get_static_maps_image

START_POINT = (37.617698, 55.755864)
START_ZOOM = 10
BASE_OFFSET = 64

IMAGE_WIDTH, IMAGE_HEIGHT = 600, 450

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

    def find_object_from_picture_cords(self, x: int, y: int):
        longitude, latitude = self._convert_picture_cords(x, y)
        self._geocoder = self._find_object_from_cords(longitude, latitude)

    def find_organiztion_from_picture_cords(self, x: int, y: int):
        longitude, latitude = self._convert_picture_cords(x, y)
        self._find_organization_from_cords(longitude, latitude)

    def _convert_picture_cords(self, x: int, y: int) -> tuple[float, float]:
        wgs84 = pyproj.CRS("EPSG:4326")

        web_mercator = pyproj.CRS("EPSG:3857")

        transformer = pyproj.Transformer.from_crs(wgs84, web_mercator, always_xy=True)

        center_x, center_y = transformer.transform(self._longitude, self._latitude)

        initial_resolution = 2 * math.pi * 6378137 / 256.0
        resolution = initial_resolution / (2 ** self._zoom)

        pixel_offset_x = x - IMAGE_WIDTH / 2
        pixel_offset_y = IMAGE_HEIGHT / 2 - y

        offset_x = pixel_offset_x * resolution
        offset_y = pixel_offset_y * resolution

        target_x = center_x + offset_x
        target_y = center_y + offset_y

        rev_transformer = pyproj.Transformer.from_crs(web_mercator, wgs84, always_xy=True)

        target_longitude, target_latitude = rev_transformer.transform(target_x, target_y)

        return target_longitude, target_latitude

    @staticmethod
    def _find_object_from_cords(longitude: float, latitude: float):
        return Geocoder.from_cords(longitude, latitude)

    def _find_organization_from_cords(self, longitude: float, latitude: float):
        new_geocoder = Geocoder.find_nearest_organization(longitude, latitude)
        distance = geopy.distance.great_circle((latitude, longitude),
                                               (new_geocoder.latitude, new_geocoder.longitude)).meters
        if distance < 50:
            self._geocoder = new_geocoder
