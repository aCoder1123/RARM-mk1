import RPi.GPIO as GPIO
from miscTest import wait as wait
GPIO.setmode(GPIO.BOARD)

ePin = 3
stepPin = 13
dirPin = 21
speed = 0.0015
steps = 1600

GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(ePin, GPIO.OUT)
GPIO.output(ePin, GPIO.LOW)


print(1)
GPIO.output(dirPin, GPIO.LOW)
for i in range(steps):
    GPIO.output(stepPin, GPIO.HIGH)
    GPIO.output(stepPin, GPIO.LOW)
    wait(speed)

print(2)
GPIO.output(dirPin, GPIO.HIGH)
for i in range(steps) :
    GPIO.output(stepPin, GPIO.HIGH)
    wait(speed)
    GPIO.output(stepPin, GPIO.LOW)
    

print("DONE")

    
GPIO.cleanup()
