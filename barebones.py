from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QGridLayout, QFileDialog)
from PyQt5.QtGui import QPixmap, QBitmap
from PyQt5.QtCore import Qt, QTimer
import sys


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.preview_screen = QApplication.primaryScreen().grabWindow(0)
        self.create_widgets()
        print(QApplication.screens())

    def create_widgets(self):
        self.img_preview = QLabel()

    def take_screenshot(self):
        self.preview_screen = QApplication.primaryScreen().grabWindow(0)
        self.img_preview.setPixmap(self.preview_screen.scaled(350, 350,
                                                              Qt.KeepAspectRatio, Qt.SmoothTransformation))

root = QApplication(sys.argv)
"""
app = MainWindow()
app.take_screenshot()
app.preview_screen.
"""
pixmap = QApplication.primaryScreen().grabWindow(
    0).scaled(500, 500, Qt.KeepAspectRatio)

print(pixmap)
