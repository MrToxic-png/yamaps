from PyQt6.QtWidgets import QMainWindow
from ui import MainWindow_ui


class MainWindow(QMainWindow, MainWindow_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
