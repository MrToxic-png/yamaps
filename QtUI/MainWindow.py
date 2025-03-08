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
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.switchThemeButton.clicked.connect(self.switch_theme)
        self.searchObjectButton.clicked.connect(self.search_object)

        self.render_map()

    def render_map(self):
        self.image.setPixmap(QPixmap(QImage.fromData(self.point_map.get_image())))

    def switch_theme(self):
        self.point_map.switch_theme()
        self.render_map()

    def search_object(self):
        self.point_map.find_toponym(self.searchObjectLineEdit.text())
        self.render_map()

    def keyPressEvent(self, a0):
        match a0.key():
            case Qt.Key.Key_PageUp:
                self.point_map.increase_zoom()
            case Qt.Key.Key_PageDown:
                self.point_map.decrease_zoom()
            case Qt.Key.Key_Up:
                self.point_map.move_up()
            case Qt.Key.Key_Down:
                self.point_map.move_down()
            case Qt.Key.Key_Left:
                self.point_map.move_left()
            case Qt.Key.Key_Right:
                self.point_map.move_right()

        self.render_map()
