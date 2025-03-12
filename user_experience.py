import os
import random
from namespaces import *
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5 import QtWidgets, QtGui, QtCore


class ExperienceEngine:
    def __init__(self, app, linkedApp):
        self.linkedApp = linkedApp
        self.app = app
        self.image_paths = [
            os.path.join(PATH_TO_IMG, f)
            for f in os.listdir(PATH_TO_IMG)
            if f.endswith(".png")
        ]
        if self.app.ds.settings["last_img"] == -1:
            self.random_image_path = PATH_TO_IMG + NAME_TITLE_IMG
        else:
            r = random.randint(0, len(self.image_paths) - 1)
            while r == self.app.ds.settings["last_img"]:
                r = random.randint(0, len(self.image_paths) - 1)

            self.random_image_path = self.image_paths[r]
            self.app.ds.settings["last_img"] = r

    def set_background(self, rescale=False):
        # print(self.image_paths)
        # ONE_TRY = False
        # Select a random image

        if self.app.ds.settings["last_img"] == -1:
            self.app.ds.settings["last_img"] = 0
            self.linkedApp.label.setText("")

        pixmap = QPixmap(self.random_image_path)
        scaled_pixmap = pixmap.scaled(
            self.linkedApp.size(),
            QtCore.Qt.KeepAspectRatioByExpanding,
            QtCore.Qt.SmoothTransformation,
        )

        # Calculate offsets for centering the image
        x_offset = (self.linkedApp.width() - scaled_pixmap.width()) // 2
        y_offset = (self.linkedApp.height() - scaled_pixmap.height()) // 2

        # Create an empty pixmap with the size of the widget
        full_pixmap = QPixmap(self.linkedApp.size())
        full_pixmap.fill(QtCore.Qt.transparent)

        # Draw the scaled pixmap onto the center of the empty pixmap
        painter = QtGui.QPainter(full_pixmap)
        painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
        painter.end()

        # Set the background image for the tab
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(full_pixmap))
        self.linkedApp.setAutoFillBackground(True)
        self.linkedApp.setPalette(palette)
