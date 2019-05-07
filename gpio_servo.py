from time import sleep
import pigpio as pg

scaleAngle = 0.08
minErr = 60
eXPrev = 0
eYPrev = 0
eXSum = 0
eYSum = 0
KP = 0.06
KD = 0.03
KI = 0.01

def initGPIO():
    try:
        p = pg.pi()
        return p
    except:
        return None

def setServoAngle(pi, pin, angle):
    '''
    pi: pigpio.pi() object
    pin: GPIO pin of servo
    angle: in degrees from 10 to 170
    '''
    assert angle >=10 and angle <= 170
    pw = (angle/18. + 3.)*200.-100.
    pi.set_servo_pulsewidth(pin, pw)
	
def updateAnglePID(servo, angleX, angleY, eX, eY):
    global eXPrev, eYPrev, eXSum, eYSum
    assert angleX >= 30 and angleX <= 150
    assert angleY >= 30 and angleY <= 150
    if eX > minErr or eX < -minErr:
        angleX += ((eX * KP) + (eXPrev * KD) + (eXSum * KI))*scaleAngle
        if angleX < 30:
            angleX = 30
        if angleX > 150:
            angleX = 150
    else:
        eXPrev = 0
        eXSum = 0
    if eY > minErr or eY < -minErr:
        angleY += ((eY * KP) + (eYPrev * KD) + (eYSum * KI))*scaleAngle
        if angleY < 30:
            angleY = 30
        if angleY > 150:
            angleY = 150
    else:
        eYPrev = 0
        eYSum = 0
    setServoAngle(xtilt, angleX)
    setServoAngle(ytilt, angleY)
    eXPrev = eX
    eYPrev = eY
    eXSum += eX
    eYSum += eY

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 1:
		setServoAngle(xtilt, 90)
		setServoAngle(ytilt, 90)
	else:
		setServoAngle(xtilt, int(sys.argv[1])) # 30 ==> 90 (middle point) ==> 150
		setServoAngle(ytilt, int(sys.argv[2])) # 30 ==> 90 (middle point) ==> 150
