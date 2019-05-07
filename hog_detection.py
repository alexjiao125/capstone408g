# import the necessary packages
#from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import time
import cv2
import numpy as np

from nms import non_max_suppression

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
        help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
        help="OpenCV object tracker type")
args = vars(ap.parse_args())
(major, minor) = cv2.__version__.split(".")[:2]
# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
if int(major) == 3 and int(minor) < 3:
        tracker = cv2.Tracker_create(args["tracker"].upper())

# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
# approrpiate object tracker constructor:
else:
        # initialize a dictionary that maps strings to their corresponding
        # OpenCV object tracker implementations
        OPENCV_OBJECT_TRACKERS = {
                "csrt": cv2.TrackerCSRT_create,
                "kcf": cv2.TrackerKCF_create,
                "boosting": cv2.TrackerBoosting_create,
                "mil": cv2.TrackerMIL_create,
                "tld": cv2.TrackerTLD_create,
                "medianflow": cv2.TrackerMedianFlow_create,
                "mosse": cv2.TrackerMOSSE_create
        }

        # grab the appropriate object tracker using our dictionary of
        # OpenCV object tracker objects
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

# initialize the bounding box coordinates of the object we are going
# to track
initBB = None
# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
        print("[INFO] starting video stream...")
        vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)
        

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the FPS throughput estimator
fps = None

#initialize HOG descriptor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# loop over frames from the video stream
while True:
        # grab the current frame, then handle if we are using a
        frame = vs.read()
        frame = cv2.flip(frame,0)
        frame = frame[1] if args.get("video", False) else frame

        # check to see if we have reached the end of the stream
        if frame is None:
                break

        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]
        #run HOG detector
         
        (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)
        
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, overlapThresh=0.65)
        areas = [np.abs((xB-xA)*(yB-yA)) for (xA, yA, xB, yB) in pick]
        if (len(areas) > 0):
            biggest_idx = np.argmax(areas)
            (xA, yA, xB, yB) = pick[biggest_idx]
            cv2.rectangle(frame, (xA,yA), (xB,yB), (0, 255, 0), 2)
        # show the output frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        fps = FPS().start()

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

# if we are using a webcam, release the pointer
if not args.get("video", False):
        vs.stop()

# otherwise, release the file pointer
else:
        vs.release()

# close all windows
camera.close()
cv2.destroyAllWindows()

