import os
import cv2
import numpy as np


class HaarcascadeDetective(object):
    def __init__(self):
        self.cascade_classifier = cv2.CascadeClassifier()

    def get_face_classifier(self):
        cur_path = os.path.split(os.path.realpath(__file__))[0]
        self.cascade_classifier.load(
            cur_path + os.path.sep + 'haarcascades' + os.path.sep + 'haarcascade_frontalface_default.xml')
        return self

    def get_face(self, image):
        handle_img = image.copy()
        gray = cv2.cvtColor(handle_img, cv2.COLOR_BGR2GRAY)
        faces = self.cascade_classifier.detectMultiScale(gray, 1.2, 10)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 1, cv2.LINE_AA)
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
