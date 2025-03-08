from dataclasses import dataclass


@dataclass
class Pointer:
    longitude: float
    latitude: float
    other_info: str | None = None

    def get_string_format(self) -> str:
        if self.other_info is None:
            return f'{self.longitude},{self.latitude}'
        return f'{self.longitude},{self.latitude},{self.other_info}'

    def __str__(self):
        return self.get_string_format()
