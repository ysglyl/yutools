# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabs.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtGui import QIcon
from daily_plan.main import YuToolsDailyPlan


class YuToolsTabsMain(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.tabs = QTabWidget(parent)
        self.tabs.setGeometry(0, 0, 805, 705)

        self.tab_daily_plan = YuToolsDailyPlan()
        self.tabs.addTab(self.tab_daily_plan, QIcon('icons/icon.png'), "Daily Plan")

        self.tab_linux_skill = QWidget(parent)
        self.tabs.addTab(self.tab_linux_skill, "Linux Skill")

        self.tab_text_handle = QWidget(parent)
        self.tabs.addTab(self.tab_text_handle, "Text Handle")

        self.tab_image_handle = QWidget(parent)
        self.tabs.addTab(self.tab_image_handle, "Image Handle")

        self.tabs.setCurrentIndex(0)
