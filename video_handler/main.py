import os
import cv2

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QFrame, QPushButton
from PyQt5.QtGui import QIcon, QImage, QPixmap
from image_handler.haarcascade_detective import HaarcascadeDetective


class YuToolsVideoHandler(QWidget):
    def __init__(self):
        super(YuToolsVideoHandler, self).__init__()

        self.flag_detect_fact = False

        self.btn_open_video = QPushButton(self)
        self.btn_open_video.setText('Open Camera')
        self.btn_open_video.setGeometry(10, 10, 80, 26)
        self.btn_open_video.clicked.connect(self.btn_click)

        self.btn_close_video = QPushButton(self)
        self.btn_close_video.setText('Close Camera')
        self.btn_close_video.setGeometry(10, 100, 80, 26)
        self.btn_close_video.clicked.connect(self.btn_click)

        self.cb_detect_fact = QCheckBox(self)
        self.cb_detect_fact.setText('Detect Face')
        self.cb_detect_fact.setGeometry(10, 40, 80, 26)
        self.cb_detect_fact.clicked.connect(self.cb_click)

        self.img_result_view = QLabel(self)
        self.img_result_view.setGeometry(340, 290, 450, 380)
        self.img_result_view.setFrameShape(QFrame.Box)
        self.img_result_view.setFrameShadow(QFrame.Sunken)
        self.img_result_view.setLineWidth(1)
        self.img_result_view.setMidLineWidth(0)
        self.img_result_view.setAlignment(Qt.AlignCenter)

    def btn_click(self):
        if self.sender() == self.btn_open_video:
            self.open_camera()
        elif self.sender() == self.btn_close_video:
            self.close_camera()

    def open_camera(self):
        self.btn_open_video.setDisabled(True)
        self.btn_close_video.setDisabled(False)
        cap = cv2.VideoCapture(0)
        success, frame = cap.read()
        while success:
            pass

    def close_camera(self):
        self.btn_open_video.setDisabled(True)
        self.btn_close_video.setDisabled(False)

    def cb_click(self):
        if self.sender() == self.cb_detect_fact:
            self.flag_detect_fact = True
        else:
            self.flag_detect_fact = False
