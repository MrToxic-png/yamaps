from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap, QImage
from QtUI.ui.MainWindow_ui import Ui_MainWindow
from yandex_maps_api import PointMap

CONST_POINT = (1, 1)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.point_map = PointMap.PointMap(CONST_POINT)

        self.render_map()

    def render_map(self):
        self.image.setPixmap(QPixmap(QImage(self.point_map.get_image())))
