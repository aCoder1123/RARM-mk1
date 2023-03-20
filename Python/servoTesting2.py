import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

servo = GPIO.PWM(11, 180)
servo.start(0)
print ("Waiting for 1 second")
time.sleep(1)
# print ("Rotating at intervals of 12 degrees")
duty = 8.5
# while duty <= 41:
#     print(duty)
#     servo.ChangeDutyCycle(duty)
#     time.sleep(.05)
#     duty = duty + 0.1 
print ("Turning back to 0 degrees")
servo.ChangeDutyCycle(8.5)
time.sleep(2)
print("zeroed")
servo.ChangeDutyCycle(41)
time.sleep(1)
print(180)
servo.ChangeDutyCycle(24.75)
time.sleep(1)
servo.ChangeDutyCycle(0)
print(90)
time.sleep(3)
servo.ChangeDutyCycle(0)
time.sleep(1)
servo.stop()
GPIO.cleanup()
print ("Everything's cleaned up")