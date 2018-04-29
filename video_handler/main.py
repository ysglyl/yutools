from threading import Thread
import os
import cv2
import time

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QCheckBox, QLabel, QFrame, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPixmap
from video_handler.haarcascade_detective import HaarcascadeDetective


class YuToolsVideoHandler(QWidget):
    def __init__(self):
        super(YuToolsVideoHandler, self).__init__()

        self.is_playing = False
        self.video_capture = None

        self.flag_detect_fact = False
        self.flag_show_gray = False

        self.btn_open_camera = QPushButton(self)
        self.btn_open_camera.setText('Open Camera')
        self.btn_open_camera.setGeometry(10, 10, 80, 26)
        self.btn_open_camera.clicked.connect(self.btn_click)

        self.btn_open_video = QPushButton(self)
        self.btn_open_video.setText('Open Video')
        self.btn_open_video.setGeometry(100, 10, 80, 26)
        self.btn_open_video.clicked.connect(self.btn_click)

        self.btn_stop_play = QPushButton(self)
        self.btn_stop_play.setText('Stop')
        self.btn_stop_play.setGeometry(190, 10, 80, 26)
        self.btn_stop_play.setDisabled(True)
        self.btn_stop_play.clicked.connect(self.btn_click)

        self.cb_detect_fact = QCheckBox(self)
        self.cb_detect_fact.setText('Detect Face')
        self.cb_detect_fact.setGeometry(10, 50, 80, 26)
        self.cb_detect_fact.clicked.connect(self.cb_click)

        self.cb_show_gray = QCheckBox(self)
        self.cb_show_gray.setText('Show Gray')
        self.cb_show_gray.setGeometry(100, 50, 80, 26)
        self.cb_show_gray.clicked.connect(self.cb_click)

        self.video_view = QLabel(self)
        self.video_view.setGeometry(80, 180, 640, 480)
        self.video_view.setFrameShape(QFrame.Box)
        self.video_view.setFrameShadow(QFrame.Sunken)
        self.video_view.setLineWidth(1)
        self.video_view.setMidLineWidth(0)
        self.video_view.setAlignment(Qt.AlignCenter)

    def btn_click(self):
        if self.sender() == self.btn_open_camera:
            self.open_camera()
        elif self.sender() == self.btn_open_video:
            self.open_video()
        elif self.sender() == self.btn_stop_play:
            self.change_btn_status((True, True, False))
            self.stop_play()

    def cb_click(self):
        if self.sender() == self.cb_detect_fact:
            if self.cb_detect_fact.isChecked():
                self.flag_detect_fact = True
            else:
                self.flag_detect_fact = False
        elif self.sender() == self.cb_show_gray:
            if self.cb_show_gray.isChecked():
                self.flag_show_gray = True
            else:
                self.flag_show_gray = False

    def open_camera(self):
        self.change_btn_status((False, False, True))
        self.video_capture = cv2.VideoCapture(0)
        self.start_play()

    def open_video(self):
        filename = QFileDialog.getOpenFileName(self, 'Select', os.path.split(os.path.realpath(__file__))[
            0] + os.path.sep + 'videos', 'Video (*.avi *.mp4 *.wmv *.mkv *.rmvb)')
        if filename[0]:
            self.change_btn_status((False, False, True))
            self.video_capture = cv2.VideoCapture(filename[0])
            self.start_play()

    def change_btn_status(self, status=(True, True, False)):
        self.btn_open_camera.setDisabled(not status[0])
        self.btn_open_video.setDisabled(not status[1])
        self.btn_stop_play.setDisabled(not status[2])

    def start_play(self):
        self.is_playing = True
        play_thread = Thread(target=self.play)
        play_thread.setDaemon(True)
        play_thread.start()

    def play(self):
        fps = self.video_capture.get(cv2.CAP_PROP_FPS)
        print(fps)
        while self.video_capture.isOpened():
            if (not self.is_playing) or (not self.parent().parent().parent().app_running):
                break
            ret, frame = self.video_capture.read()
            if ret:
                pipe, fmt, handled_frame = self.handle_image(frame)
                q_image = QImage(handled_frame, handled_frame.shape[1], handled_frame.shape[0],
                                 handled_frame.shape[1] * pipe, fmt)
                q_pixmap = QPixmap.fromImage(q_image)
                q_pixmap = q_pixmap.scaled(640, 480, Qt.KeepAspectRatio)
                self.video_view.setPixmap(q_pixmap)
            if fps != 0:
                time.sleep(1.0 / fps)

        self.video_view.clear()
        self.video_capture.release()

    def stop_play(self):
        self.is_playing = False

    def handle_image(self, image):
        pipe = 3
        fmt = QImage.Format_RGB888
        flag_handle = False
        if self.flag_detect_fact:
            image = HaarcascadeDetective().get_face_classifier().get_face(image)
            flag_handle = True
        if self.flag_show_gray:
            pipe = 1
            fmt = QImage.Format_Grayscale8
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            flag_handle = True
        if not flag_handle:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return pipe, fmt, image
