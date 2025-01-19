from time import sleep
import cv2 
from deepface import DeepFace 
import matplotlib.pyplot as plt 



class FaceExpression():

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.read()

    def getFrame(self):
        _, frame = self.cam.read()
        return frame
    
    def getEmotion(self):

        img = self.getFrame()
        # img = cv2.imread("/Users/nawaf/Documents/GitHub/BlockedIn-Backend/Photo on 2025-01-18 at 11.44 AM.jpg")
        # cv2.imwrite("img_name.png", img)
        # call imshow() using plt object 

        try :
            result = DeepFace.analyze(img,actions=['emotion'])
        except ValueError as e:
            if str(e) == 'Face could not be detected in numpy array.Please confirm that the picture is a face photo or consider to set enforce_detection param to False.':
                return 999
            else:
                raise e


        dominant_emotion = result[0]['dominant_emotion']
        return dominant_emotion
    

    def end(self):
        self.cam.release()