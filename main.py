import sys
from functools import partial

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *  # QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt5.QtCore import *

from ui import Ui_MainWindow
from namespaces import *
from modules import *
from classes import *
from saver import *

namespacesInit()


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ds = DataSaver(self)

        self.resize(self.ds.settings["x"], self.ds.settings["y"])

        if self.ds.settings["full_screen"] == 1:
            self.showMaximized()
        else:
            self.showNormal()

        # connect func create new tab (HomeTab)
        self.ui.pushButton_general_open.clicked.connect(
            partial(self.create_tab, self, self, HomeTab)
        )

        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.ui.tabWidget.setMovable(True)

    def create_tab(
        self, selfModifi, selfLinked, tab_class, title="", title2line="", content=None
    ):
        tab = tab_class(selfModifi, selfLinked, title)
        self.ui.tabWidget.addTab(
            tab, tab.title + (f"\n{title2line}" if title2line else "")
        )
        self.ui.tabWidget.setCurrentIndex(self.ui.tabWidget.count() - 1)

    def close_tab(self, index):
        self.ui.tabWidget.removeTab(index)

    def showWarning(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def showDialog(
        self, message, title="Warning", button_text=("OK", "Cancel"), set_icon_flag=True
    ):
        # Создаем диалоговое окно
        msg_box = QMessageBox()

        if set_icon_flag:
            msg_box.setIcon(QMessageBox.Warning)

        msg_box.setWindowTitle(title)
        msg_box.setText(message)

        left_button = msg_box.addButton(button_text[0], QMessageBox.AcceptRole)
        right_button = msg_box.addButton(button_text[1], QMessageBox.RejectRole)

        msg_box.exec_()
        return msg_box.clickedButton() == left_button

    def resizeEvent(self, event):
        # Передаем событие обработчику изменения размера
        # self.resizeHandler.resizeEvent(event)
        # Вызов базового метода resizeEvent
        QTimer.singleShot(0, self.handle_event)
        super().resizeEvent(event)

    def handle_event(self):
        if self.ds.settings["full_screen"] == 0:
            self.ds.save_window_size(self)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:

            if self.isMaximized():
                # print("Window state: Maximized")
                self.ds.settings["full_screen"] = 1
            else:
                # print("Window state: More")
                self.ds.settings["full_screen"] = 0
        super().changeEvent(event)

    def closeEvent(self, event):
        self.ds.global_save()
        super().closeEvent(event)


if __name__ == "__main__":
    print("hello")
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(PATH_TO_ICON))
    myApp = MyApp()
    myApp.show()
    sys.exit(app.exec_())
