#Current limits of gimbal as of 5/8/19: DO NOT EXCEED 30<X<140 AND 80<Y<160.
#Y = 0 is pointed to the ceiling and X = 0 is pointed laterally away from the side of the Pi where the GPIO pins are located. These limits are in place for the protection of the servos and the ribbon cable. Be cognizant if changes to the angle are made in the gpio_servo library. These bounds might not hold. 


from time import sleep
import gpio_servo as servo
pi = servo.initGPIO()
servo.xtilt = 17
servo.ytilt = 27
for i in range(20,160,2):
    servo.setServoAngle(pi,servo.xtilt,i)
    print("Just moved xy plane")
    sleep(0.5)
    servo.setServoAngle(pi,servo.ytilt,i)
    print("Just moved yz plane")
    sleep(0.5)
for i in range (160,20,-2):
    servo.setServoAngle(pi,servo.xtilt, i)
    sleep(0.5)
    servo.setServoAngle(pi,servo.ytilt, i)
    sleep(0.5)
    
