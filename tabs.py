# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tabs.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QWidget, QTabWidget
from PyQt5.QtGui import QIcon
from daily_plan.main import YuToolsDailyPlan
from statistics_word_en.main import YuToolsStatisticsWordEn
from note_viewer.main import YuToolsNoteViewer
from image_handler.main import YuToolsImageHandler


class YuToolsTabsMain(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.tabs = QTabWidget(parent)
        self.tabs.setGeometry(0, 0, 805, 705)

        self.tab_note_viewer = YuToolsNoteViewer()
        self.tabs.addTab(self.tab_note_viewer, QIcon('icons/note_viewer.png'), 'Note Viewer')

        self.tab_daily_plan = YuToolsDailyPlan()
        self.tabs.addTab(self.tab_daily_plan, QIcon('icons/daily_plan.png'), "Daily Plan")

        self.tab_statistics_word_en = YuToolsStatisticsWordEn()
        self.tabs.addTab(self.tab_statistics_word_en, QIcon('icons/statistics_word_en.png'), "Statistics EN")

        self.tab_image_handler = YuToolsImageHandler()
        self.tabs.addTab(self.tab_image_handler, QIcon('icons/image_handler.png'), 'Image Handler')

        self.tabs.setCurrentIndex(0)
