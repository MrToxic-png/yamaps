from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap, QImage
from  PyQt6.QtCore import Qt
from .ui import Ui_MainWindow
from yandex_maps_api import PointMap


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.point_map = PointMap()

        self.render_map()

    def render_map(self):
        self.image.setPixmap(QPixmap(QImage.fromData(self.point_map.get_image())))

    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_PageUp:
            self.point_map.increase_zoom()
        if a0.key() == Qt.Key.Key_PageDown:
            self.point_map.decrease_zoom()

        self.render_map()
