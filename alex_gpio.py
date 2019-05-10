#uses pigpio library for software pwm
from time import sleep
import pigpio as pg

#all units in the next 9 lines are in degrees
scaleAngle = 0.96
minErr = 2 
eXPrev = 0
eYPrev = 0
eXSum = 0
eYSum = 0
KP = 0.5 
KD = 0.28
KI = 0.006

angleX = 0
angleY = 0

#These are the limits of the gimbal to protect the ribbon cable and servo
#from damage. Last updated: 5/8/19
xMin = 30
xMax = 140
yMin = 80
yMax = 160

#must initialize these two variables from python script.
#ex: gpio_servo.xtilt = 17 and gpio_servo.ytilt = 27
xtilt=17
ytilt=27

def initGPIO():
    global xtilt, ytilt, angleX, angleY
    try:
        pi = pg.pi()
        angleX = 90
        angleY = 110
        setServoAngle(pi, xtilt, angleX)
        setServoAngle(pi, ytilt, angleY)
        return pi
    except:
        return None

def setServoAngle(pi, pin, angle):
    '''
    pi: pigpio.pi() object
    pin: GPIO pin of servo
    angle: in degrees from 10 to 170
    '''
    #ensure the pins for the servos have been initialized
    assert xtilt > 0 and ytilt > 0
    if(pin==xtilt):
        if(angle > xMax):
            angle = xMax
        elif(angle < xMin):
            angle = xMin
        angleX = angle
    elif(pin==ytilt):
        if(angle > yMax):
            angle = yMax
        elif(angle < yMin):
            angle = yMin
        angleY = angle
    else:
        assert False, "you havent' initialized xtilt and ytilt pins on Rpi. Try: gpio_servo.xtilt = NUMBER for example"
    pw = (angle/18. + 3.)*200.-100.
    pi.set_servo_pulsewidth(pin, pw)
	
def updateAnglePID(servo, eX, eY):
    assert xtilt > 0 and ytilt > 0, "ensure xtilt, ytilt have been set in gpio_servo.py module"
    global eXPrev, eYPrev, eXSum, eYSum, angleX, angleY
    if eX > minErr or eX < -minErr:
        angleX -= ((eX * KP) + (eXPrev * KD) + (eXSum * KI))*scaleAngle
        if angleX < xMin:
            angleX = xMin
        if angleX > xMax:
            angleX = xMax
    else:
        eXPrev = 0
        eXSum = 0
    if eY > minErr or eY < -minErr:
        angleY += ((eY * KP) + (eYPrev * KD) + (eYSum * KI))*scaleAngle
        if angleY < yMin:
            angleY = yMin
        if angleY > yMax:
            angleY = yMax
    else:
        eYPrev = 0
        eYSum = 0
    if(eXPrev != 0):
        setServoAngle(servo, xtilt, angleX)
    if(eYPrev != 0):
        setServoAngle(servo, ytilt, angleY)
    eXPrev = eX
    eYPrev = eY
    eXSum += eX
    eYSum += eY
    print("angleX: ", angleX, " angleY: ", angleY)

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 1:
		setServoAngle(xtilt, 90)
		setServoAngle(ytilt, 90)
	else:
		setServoAngle(xtilt, int(sys.argv[1])) # 30 ==> 90 (middle point) ==> 150
		setServoAngle(ytilt, int(sys.argv[2])) # 30 ==> 90 (middle point) ==> 150
