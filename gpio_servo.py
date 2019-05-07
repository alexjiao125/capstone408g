#uses pigpio library for software pwm
from time import sleep
import pigpio as pg

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
	
def updateAngle(servo, angleX, angleY, tarX, tarY):
    scaleAngle = 1
    assert angleX >= 30 and angleX <= 150
    assert angleY >= 30 and angleY <= 150
    if tarX > 5 or tarX < -5:
        angleX = angleX + round(scaleAngle*tarX)
        if angleX < 30:
            angleX = 30
        if angleX > 150:
            angleX = 150
    if tarY > 5 or tarY < -5:
        angleY = angleY + round(scaleAngle*tarX)
        if angleY < 30:
            angleY = 30
        if angleY > 150:
            angleY = 150
    setServoAngle(xtilt, angleX)
    setServoAngle(ytilt, angleY)
if __name__ == '__main__':
	import sys
	if len(sys.argv) == 1:
		setServoAngle(xtilt, 90)
		setServoAngle(ytilt, 90)
	else:
		setServoAngle(xtilt, int(sys.argv[1])) # 30 ==> 90 (middle point) ==> 150
		setServoAngle(ytilt, int(sys.argv[2])) # 30 ==> 90 (middle point) ==> 150
