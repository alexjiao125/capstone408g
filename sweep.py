from time import sleep
import gpio_servo as servo
pi = servo.initGPIO()
xtilt = 17
ytilt = 27
for i in range(10,50,2):
    servo.setServoAngle(pi,ytilt,i)
    sleep(1)
for i in range (50,10,-2):
    servo.setServoAngle(pi,ytilt, i)
    sleep(1)
    
