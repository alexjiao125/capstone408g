# import the necessary packages
#from imutils.video import VideoStream
import cv2
import numpy as np

#from nms import non_max_suppression

def get_BB_hog(frame, hog):
        #initialize HOG descriptor
        #hog = cv2.HOGDescriptor()
        #hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        (H, W) = frame.shape[:2]
        #run HOG detector
        (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
                        
        #rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        #pick = non_max_suppression(rects, overlapThresh=0.65)
        pick = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        areas = [np.abs((xB-xA)*(yB-yA)) for (xA, yA, xB, yB) in pick]
        if (len(areas) > 0):
               (xA, yA, xB, yB) = pick[np.argmax(areas)]
               return xA, yA, xB, yB 
        else:
               return None

