# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 613)
        self.main_tabs = QtWidgets.QWidget(MainWindow)
        self.main_tabs.setObjectName("main_tabs")
        self.tabWidget = QtWidgets.QTabWidget(self.main_tabs)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 561))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_daily_plan = QtWidgets.QWidget()
        self.tab_daily_plan.setObjectName("tab_daily_plan")
        self.textEdit = QtWidgets.QTextEdit(self.tab_daily_plan)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 341, 71))
        self.textEdit.setObjectName("textEdit")
        self.spinBox = QtWidgets.QSpinBox(self.tab_daily_plan)
        self.spinBox.setGeometry(QtCore.QRect(110, 110, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.comboBox = QtWidgets.QComboBox(self.tab_daily_plan)
        self.comboBox.setGeometry(QtCore.QRect(10, 110, 69, 22))
        self.comboBox.setObjectName("comboBox")
        self.checkBox = QtWidgets.QCheckBox(self.tab_daily_plan)
        self.checkBox.setGeometry(QtCore.QRect(180, 110, 70, 17))
        self.checkBox.setObjectName("checkBox")
        self.dateEdit = QtWidgets.QDateEdit(self.tab_daily_plan)
        self.dateEdit.setGeometry(QtCore.QRect(10, 150, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.tab_daily_plan)
        self.dateEdit_2.setGeometry(QtCore.QRect(140, 150, 110, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_daily_plan)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 190, 69, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_daily_plan)
        self.comboBox_3.setGeometry(QtCore.QRect(100, 190, 69, 22))
        self.comboBox_3.setObjectName("comboBox_3")
        self.pushButton = QtWidgets.QPushButton(self.tab_daily_plan)
        self.pushButton.setGeometry(QtCore.QRect(10, 230, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab_daily_plan, "")
        self.tab_linux_skill = QtWidgets.QWidget()
        self.tab_linux_skill.setObjectName("tab_linux_skill")
        self.tabWidget.addTab(self.tab_linux_skill, "")
        self.tab_text_handle = QtWidgets.QWidget()
        self.tab_text_handle.setObjectName("tab_text_handle")
        self.tabWidget.addTab(self.tab_text_handle, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        MainWindow.setCentralWidget(self.main_tabs)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.pushButton.released.connect(self.pushButton.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_daily_plan), _translate("MainWindow", "Daily Plan"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_linux_skill), _translate("MainWindow", "Linux Skill"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_text_handle), _translate("MainWindow", "Text Handle"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Image Handle"))

