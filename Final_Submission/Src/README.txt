This subdirectory contains all the code for our project. 

Refer to the User Manual in Doc/ for setting up Raspbian and the 
Python environment prior to running any of the code.

The file integrated.py contains the basic code that allows a user to 
select a region of interesti (ROI) and then have the camera track an
object within that ROI. To run this:
- ensure that integrated.py and gpio_servo.py are in the same directory.
- Activate the Python environment if not already activated.
- Run the script by typing "python3 integrated.py -t mosse"
- A screen should pop up displaying the camera feed. To select an ROI 
  press the "s" key then use the mouse to drag over the desired region. 
  Press "c" to cancel the selection.
- After the ROI is selected the tracker should start following the object.
- At any point, press "s" to select a new ROI or "q" to exit the program.

The file hog_integrated.py contains the code that uses HOG to detect 
bounding boxes around people instead of having a user select them. To run
this code: 
- ensure that hog_integrated.py, hog_bb.py, and gpio_servo.py are 
  all in the same directory.
- Activate the Python environment if not already activated.
- Run the script by typing "python3 hog_integrated.py -w $POSINT$", replacing
  $POSINT$ with some positive integer; 30 is the default. This integer is 
  the number of frames to wait before recomputing HOG if the bounding box is 
  either lost or stationary. See the report in Doc/ for more details on this.
- A screen should pop up displaying the camera feed. The script should start HOG
  to find a bounding box around any person. If the camera feed ever freezes, it is
  due to HOG being run which slows down the program.
- At any point, press "q" to exit the program.

