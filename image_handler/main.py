import os
import cv2
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPixmap
from image_handler.haarcascade_detective import HaarcascadeDetective


class YuToolsImageHandler(QWidget):
    def __init__(self):
        super(YuToolsImageHandler, self).__init__()

        self.btn_detect_face = QPushButton(self)
        self.btn_detect_face.setText('Detect Face')
        self.btn_detect_face.setGeometry(10, 10, 80, 26)
        self.btn_detect_face.clicked.connect(self.click_handle)

        self.btn_show_gray = QPushButton(self)
        self.btn_show_gray.setText('Gray')
        self.btn_show_gray.setGeometry(100, 10, 80, 26)
        self.btn_show_gray.clicked.connect(self.click_handle)

        self.img_major_view = QPushButton(self)
        self.img_major_view.setGeometry(340, 10, 220, 220)
        self.img_major_view.setIcon(QIcon('icons/image_handler/default.png'))
        self.img_major_view.setIconSize(QSize(215, 215))
        self.img_major_view.clicked.connect(self.select_image)
        self.img_major = os.path.realpath('icons/image_handler/default.png')

        self.img_minor_view = QPushButton(self)
        self.img_minor_view.setGeometry(570, 10, 220, 220)
        self.img_minor_view.setIcon(QIcon('icons/image_handler/default.png'))
        self.img_minor_view.setIconSize(QSize(215, 215))
        self.img_minor_view.clicked.connect(self.select_image)
        self.img_minor = os.path.realpath('icons/image_handler/default.png')

        self.lbl_result = QLabel(self)
        self.lbl_result.setText('Nothing is handling')
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setGeometry(340, 235, 450, 50)
        self.lbl_result.setFrameShape(QFrame.Box)
        self.lbl_result.setFrameShadow(QFrame.Sunken)
        self.lbl_result.setLineWidth(1)
        self.lbl_result.setMidLineWidth(0)
        self.lbl_result.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.img_result_view = QLabel(self)
        self.img_result_view.setGeometry(340, 290, 450, 380)
        self.img_result_view.setFrameShape(QFrame.Box)
        self.img_result_view.setFrameShadow(QFrame.Sunken)
        self.img_result_view.setLineWidth(1)
        self.img_result_view.setMidLineWidth(0)
        self.img_result_view.setAlignment(Qt.AlignCenter)

    def select_image(self):
        btn = self.sender()
        filename = QFileDialog.getOpenFileName(self, 'Select', os.path.split(os.path.realpath(__file__))[
            0] + os.path.sep + 'images', 'Images (*.png *.jpg)')
        if btn == self.img_major_view:
            if filename[0]:
                self.img_major = filename[0]
                self.img_major_view.setIcon(QIcon(self.img_major))
        elif btn == self.img_minor_view:
            if filename[0]:
                self.img_minor = filename[0]
                self.img_minor_view.setIcon(QIcon(self.img_minor))

    def click_handle(self):
        btn = self.sender()
        if btn == self.btn_detect_face:
            pipe, img = HaarcascadeDetective().get_face_classifier().get_face(self.img_major)
            if pipe == 0:
                return
            if pipe == 3:
                fmt = QImage.Format_RGB888
            elif pipe == 4:
                fmt = QImage.Format_RGBA8888
        elif btn == self.btn_show_gray:
            img = cv2.imread(self.img_major, 0)
            fmt = QImage.Format_Grayscale8
            pipe = 1
        q_image = QImage(img, img.shape[1], img.shape[0], img.shape[1] * pipe, fmt)
        q_pixmap = QPixmap.fromImage(q_image)
        q_pixmap = q_pixmap.scaled(450, 380, Qt.KeepAspectRatio)
        self.img_result_view.setPixmap(q_pixmap)
