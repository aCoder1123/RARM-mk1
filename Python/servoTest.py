from gpiozero import AngularServo
from time import sleep

servo = AngularServo(17, min_angle=-90, max_angle=90)

while True:
    servo.angle = -90
    sleep(2)
    servo.min()
    sleep(2)
    servo.angle = 0
    sleep(2)
    servo.angle = 90
    sleep(2)
    

# from gpiozero import Servo
# from time import sleep
# servo = Servo(17)

# while True:
#     servo.value = 2
#     sleep(2)
#     servo.value = 0
#     sleep(2)
#     # servo.value(-1)
#     # sleep(2)