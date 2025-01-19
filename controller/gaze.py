import cv2

import sys
from gazetracking import GazeTracking


gaze = GazeTracking()

class GazeData:
    def __init__(self):
        self.gaze = GazeTracking()
        self.webcam = cv2.VideoCapture(0)

    def getFrame(self):
        _, frame = self.webcam.read()
        self.gaze.refresh(frame)
        frame = self.gaze.annotated_frame()
        return frame
    
    def getGaze(self):
        frame = self.getFrame()
        gaze.refresh(frame)
        text = 0
        if gaze.is_blinking():
            text = 1
        elif gaze.is_right():
            text = 2
        elif gaze.is_left():
            text = 3
        elif gaze.is_center():
            text = 4

    
        return text

    def end(self):
        self.webcam.release()


