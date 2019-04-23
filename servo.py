from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
xtilt = 27
ytilt = 17
scaleAngle = 1
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
def updateAngle(servo, angleX, angleY, tarX, tarY):
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
	GPIO.cleanup()