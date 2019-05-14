#uses pigpio library for software pwm
from time import sleep, time
import pigpio as pg

#all units in the next 9 lines are in degrees
scaleAngle = 0.96
minErr = 2 
maxRotation = 0.6
eXPrev = 1e-12 
eYPrev = 1e-12 
eXSum = 0
eYSum = 0
KPx =0.02 #0.1 
KPy =0.01 #0.05  
KDx =0.014 #0.0 
KDy =0.006  #0.0
KIx =0.012 #0.0 
KIy =0.006 #0.0 
lastTime = 0

angleX = 0
angleY = 0

#These are the limits of the gimbal to protect the ribbon cable and servo
#from damage. Last updated: 5/8/19
xMin = 30
xMax = 155
yMin = 90
yMax = 160

#must initialize these two variables from python script.
#ex: gpio_servo.xtilt = 17 and gpio_servo.ytilt = 27
xtilt=17
ytilt=27

def initGPIO():
    global xtilt, ytilt, angleX, angleY, lastTime
    try:
        pi = pg.pi()
        angleX = 95 
        angleY = 95 
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
    global eXPrev, eYPrev, eXSum, eYSum, angleX, angleY, lastTime
    if eX > minErr or eX < -minErr:
        Xchange = ((eX * KPx) + (eXPrev * KDx) + (eXSum * KIx))*scaleAngle
        #we don't want any particular adjustment to be too large, or the image becomes blurry and MOSSE will lose the person.
        #if the amount of error accumulated ( = Xchange) is above the threshold, only adjust the angle by the max threshold
        if(abs(Xchange)>maxRotation): #
            angleX -= maxRotation*((Xchange>0)*2-1)
        else:
            angleX -= Xchange
        #print("Angle error X: ", (eX * KPx)*scaleAngle , (eXPrev * KDx)*scaleAngle , (eXSum * KIx)*scaleAngle)
        if angleX < xMin:
            angleX = xMin
        if angleX > xMax:
            angleX = xMax
    else:
        eXPrev = 0
        eXSum = 0
    if eY > minErr or eY < -minErr:
        Ychange = ((eY * KPy) + (eYPrev * KDy) + (eYSum * KIy))*scaleAngle
        if(abs(Ychange)>maxRotation):
            angleY += maxRotation*((Ychange>0)*2-1)
        else:
            angleY += Ychange
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
    eXSum += eX*(time()-lastTime)
    eYSum += eY*(time()-lastTime)
    lastTime = time()
    #print("angleX: ", angleX, " angleY: ", angleY)

if __name__ == '__main__':
	import sys
	pi = initGPIO()
	if len(sys.argv) == 1:
		setServoAngle(pi,xtilt, 90)
		setServoAngle(pi,ytilt, 90)
	else:
		setServoAngle(pi,xtilt, int(sys.argv[1])) # 30 ==> 90 (middle point) ==> 150
		setServoAngle(pi,ytilt, int(sys.argv[2])) # 30 ==> 90 (middle point) ==> 150
