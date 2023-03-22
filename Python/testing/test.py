#test file for working with stepper motor and driver

import RPi.GPIO as GPIO
from time import sleep
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(75, GPIO.OUT) 
# GPIO.setup(5, GPIO.OUT)
# GPIO.output(5, GPIO.LOW)
# GPIO.setup(7, GPIO.OUT)
# GPIO.output(7, GPIO.LOW)
x =1
for i in range(0, 300): #pulse generation to tell the stepper driver to move
    print(x)
    x+=1
    GPIO.output(7, (GPIO.HIGH))
    sleep(0.02)
    GPIO.output(7, (GPIO.LOW))
    sleep(0.02)
            
print("stopping")
# GPIO.output(7, GPIO.LOW)
GPIO.cleanup()
