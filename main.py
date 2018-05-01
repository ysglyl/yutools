# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.py'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtGui import QIcon

from tabs import YuToolsTabsMain


class YuToolsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_running = True
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(803, 705)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setWindowIcon(QIcon('icons/icon.png'))
        self.setWindowTitle('YuTools')

    def closeEvent(self, *args, **kwargs):
        self.app_running = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = YuToolsMainWindow()
    tabs = YuToolsTabsMain(win)
    win.show()
    sys.exit(app.exec_())
