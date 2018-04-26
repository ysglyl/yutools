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
        img = cv2.imread(image, -1)
        handle_img = img.copy()
        gray = cv2.cvtColor(handle_img, cv2.COLOR_BGR2GRAY)
        faces = self.cascade_classifier.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1, cv2.LINE_AA)
        if len(img[0][0]) == 4:
            b, g, r, a = cv2.split(img)
            return 4, cv2.merge([r, g, b, a])
        elif len(img[0][0] == 3):
            b, g, r = cv2.split(img)
            return 3, cv2.merge([r, g, b])
        return 0, None
