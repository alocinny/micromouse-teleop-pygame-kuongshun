import cv2
import pygame
import numpy as np


class CameraViewer:
    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(source)

    def is_opened(self) -> bool:
        return self.cap.isOpened()

    def read_surface(self, target_size=None):
        if not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if target_size is not None:
            frame = cv2.resize(frame, target_size)

        frame = np.rot90(frame)
        surface = pygame.surfarray.make_surface(frame)

        return surface

    def release(self):
        self.cap.release()
