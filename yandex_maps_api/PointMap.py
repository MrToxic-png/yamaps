from .static_maps import get_static_maps_image


START_POINT = (37.617698, 55.755864)
START_ZOOM = 10


class PointMap:
    def __init__(self):
        self._point = START_POINT
        self._zoom = START_ZOOM

    def get_image(self) -> bytes:
        return get_static_maps_image(*self._point, self._zoom)

    def decrease_zoom(self):
        self._zoom = max(self._zoom - 1, 0)

    def increase_zoom(self):
        self._zoom = min((self._zoom + 1, 21))
