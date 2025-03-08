from .static_maps import get_static_maps_image


START_POINT = (37.617698, 55.755864)
START_ZOOM = 10
BASE_OFFSET = 64


class PointMap:
    def __init__(self):
        self._longitude, self._latitude = START_POINT
        self._zoom = START_ZOOM

    def get_image(self) -> bytes:
        return get_static_maps_image(self._longitude, self._latitude, self._zoom)

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

