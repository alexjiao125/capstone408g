import numpy as np
import cv2 as cv
cap = cv.VideoCapture('People_walking_in_airport.mov')

fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
while(1):
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame)
#    cv.imshow('frame',gray)
    cv.imshow('frame',fgmask)
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()

