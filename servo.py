from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
xtilt = 27
ytilt = 17
scaleAngle = 0.08
minErr = 60
eXPrev = 0
eYPrev = 0
eXSum = 0
eYSum = 0
KP = 0.06
KD = 0.03
KI = 0.01
GPIO.setup(xtilt, GPIO.OUT) # white => TILT
GPIO.setup(ytilt, GPIO.OUT) # gray ==> PAN
def setServoAngle(servo, angle):
	assert angle >=30 and angle <= 150
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()
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
	GPIO.cleanup()