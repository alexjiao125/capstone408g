# import the necessary packages
import argparse
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import time
import cv2
import gpio_servo as servo
from hog_bb import get_BB_hog

first_version_tracker = 1

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
        help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="mosse",
        help="OpenCV object tracker type")
ap.add_argument("-w", "--wait", type=int, default=15,
        help="How many frames to wait before calling HoG")
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
        first_version_tracker = 0
        # grab the appropriate object tracker using our dictionary of
        # OpenCV object tracker objects
        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

#initialize counter to see how long its been since a bb was found by mosse
start_hog = args["wait"] 
n_frames = 0

#initialize counter to see if bb is static
static_frame_thresh = 150   #args["wait"] 
change_thresh = 4 
n_static = 0
last_box = [0, 0, 0, 0]

#initialize HOG descriptor
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#flag to know when to start HOG
run_hog = True

#initialize the pins to control the servos on the Rpi
servo.xtilt = 17
servo.ytilt = 27
pi = servo.initGPIO()

captureResolution = (1080,720)
degreesPerWidth = 62.2
degreesPerHeight = 48.8

# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
        print("[INFO] starting video stream...")
        vs = VideoStream(usePiCamera=True,resolution = captureResolution).start()
        print("test0")
        time.sleep(2.0)
        

# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])

# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
while True:
        # grab the current frame, then flip 
        frame = vs.read()
        frame = cv2.flip(frame,0) #flip frame vertically
        frame = cv2.flip(frame,1) #flip frame horizontally
        frame = frame[1] if args.get("video", False) else frame

        # check to see if we have reached the end of the stream
        if frame is None:
                break

        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        frame = imutils.resize(frame, height=512)
        (H, W) = frame.shape[:2]

        # check to see if we are currently tracking an object
        if initBB is not None:
                # grab the new bounding box coordinates of the object
                (success, box) = tracker.update(frame)

                # check to see if the tracking was a success
                #if so, obtain the center of the rectangle and move the gimbal accordingly
                if success:
                        (x, y, w, h) = [int(v) for v in box]
                        change = (x+w/2-last_box[0]-last_box[2]/2)**2 + (y+h/2-last_box[1]-last_box[3]/2)**2
                        if(change < change_thresh):
                                n_static += 1
                                if(n_static == static_frame_thresh):
                                        print('Static thresh reached')
                                        #initBB = None
                                        n_static = 0
                                        #continue
                                        run_hog = True
                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                (0, 255, 0), 2)
                        cX = int((w/2)+x)
                        cY = int((h/2)+y)
                        originX = int(W/2)
                        originY = int(H/2)
                        errorX = (cX-originX)*(degreesPerWidth/W)
                        errorY = (cY-originY)*(degreesPerHeight/H)
                        #print('error x: ',errorX,' error y: ', errorY)
                        servo.updateAnglePID(pi,errorX,errorY)
                        last_box[0] = x
                        last_box[1] = y
                        last_box[2] = w
                        last_box[3] = h
                else:
                        n_frames += 1
                        if(n_frames == start_hog):
                                print('Lost bb thresh reached')
                                #initBB = None
                                n_frames = 0
                                #continue
                                run_hog = True
                # update the FPS counter
                fps.update()
                fps.stop()

                # initialize the set of information we'll be displaying on
                # the frame
                info = [
                        ("Tracker", args["tracker"]),
                        ("Success", "Yes" if success else "No"),
                        ("FPS", "{:.2f}".format(fps.fps())),
                ]
                # loop over the info tuples and draw them on our frame
                for (i, (k, v)) in enumerate(info):
                        text = "{}: {}".format(k, v)
                        cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        # show the output frame
        
        #if there is no current bounding box, use hog to find one
        if (initBB is None) or (run_hog is True):
                # select the bounding box of the object we want to track (make
                # sure you press ENTER or SPACE after selecting the ROI)
                initBB = get_BB_hog(frame, hog)
                if(initBB is None):
                        continue
                
                cv2.rectangle(frame,(initBB[0],initBB[1]),
                        (initBB[0]+initBB[2],initBB[1]+initBB[3]),(0,255,0),2) 
                # start OpenCV object tracker using the supplied bounding box
                # coordinates, then start the FPS throughput estimator as well
                #initBB_xywh = list(initBB)
                #initBB_xywh[2] = initBB[2]-initBB[0]
                #initBB_xywh[3] = initBB[3]-initBB[1]
                if(first_version_tracker):
                        tracker = cv2.Tracker_create(args["tracker"].upper())
                else:
                        tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
                tracker.init(frame, initBB)
                servo.eXSum = 0
                servo.eYSum = 0
                servo.eXPrev = 0
                servo.eYPrev = 0
                servo.lastTime = time.time()
                print("INIT BB:", initBB)
                fps = FPS().start()
                run_hog = False

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

# if we are using a webcam, release the pointer

# otherwise, release the file pointer
else:
        vs.release()

# close all windows
cv2.destroyAllWindows()

#Note: suppose the optional Resolution parameter in the vs.videoStream line was set to 64x64 pixels.
#Then, let's say we do cv2.resize to width = 500. Then what you will see on the screen is a box that
#takes up 500 columns of pixels on the monitor, but there are only 64 cubes, or blocks shown across those 500 columns.
#I.e. the image appears very pixelated. What we're doing is only using 64x64 sensors from the camera and upsampling so that
#those 64 pixels are shown across 500 columns.
