import numpy as np
import argparse
import cv2
import PIL
import matplotlib.pyplot as plt

from nms import non_max_suppression

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# load the image and resize it to (1) reduce detection time
# and (2) improve detection accuracy
filename = 'Pedestrians.jpg'
image = PIL.Image.open(filename)
width, height = image.size
new_width = min(400, width)
#image = image.resize((new_width, height))
image = np.array(image)
orig = image.copy()

# detect people in the image
(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
	padding=(8, 8), scale=1.05)
 
# draw the original bounding boxes
for (x, y, w, h) in rects:
	cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
# apply non-maxima suppression to the bounding boxes using a
# fairly large overlap threshold to try to maintain overlapping
# boxes that are still people
rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
pick = non_max_suppression(rects, overlapThresh=0.65)
 
# draw the final bounding boxes
for (xA, yA, xB, yB) in pick:
	cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
 
# show some information on the number of bounding boxes
print("[INFO] {}: {} original boxes, {} after suppression".format(
	filename, len(rects), len(pick)))
 
# show the output images
f1 = plt.figure(1)
plt.imshow(orig)
plt.title('Original')
f2 = plt.figure(2)
plt.imshow(image)
plt.title('After NMS')
plt.show()

