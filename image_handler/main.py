import os
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QGraphicsView, QPushButton, QLabel, QFrame,QFileDialog
from PyQt5.QtGui import QFont, QIcon


class YuToolsImageHandler(QWidget):
    def __init__(self):
        super(YuToolsImageHandler, self).__init__()

        self.img_major = QPushButton(self)
        self.img_major.setGeometry(340, 10, 220, 220)
        self.img_major.setIcon(QIcon('icons/image_handler/default.png'))
        self.img_major.setIconSize(QSize(220, 220))
        self.img_major.clicked.connect(self.select_image)

        self.img_minor = QPushButton(self)
        self.img_minor.setGeometry(570, 10, 220, 220)
        self.img_minor.setIcon(QIcon('icons/image_handler/default.png'))
        self.img_minor.setIconSize(QSize(220, 220))
        self.img_minor.clicked.connect(self.select_image)

        self.lbl_result = QLabel(self)
        self.lbl_result.setText('Nothing is handling')
        self.lbl_result.setWordWrap(True)
        self.lbl_result.setGeometry(340, 235, 450, 50)
        self.lbl_result.setFrameShape(QFrame.Box)
        self.lbl_result.setFrameShadow(QFrame.Sunken)
        self.lbl_result.setLineWidth(1)
        self.lbl_result.setMidLineWidth(0)
        self.lbl_result.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)

        self.gv_result = QGraphicsView(self)
        self.gv_result.setGeometry(340, 290, 450, 380)

    def select_image(self):
        btn = self.sender()
        QFileDialog.getOpenFileName()
        if btn == self.img_major:
            pass
        elif btn == self.img_minor:
            pass
