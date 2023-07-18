import RPi.GPIO as GPIO
from miscTest import wait as wait
GPIO.setmode(GPIO.BOARD)

stepPin = 3
dirPin = 5
speed = 0.001

GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

print(1)
GPIO.output(dirPin, GPIO.LOW)
for i in range(1600):
    GPIO.output(stepPin, GPIO.HIGH)
    GPIO.output(stepPin, GPIO.LOW)
    wait(speed)

print(2)
GPIO.output(dirPin, GPIO.HIGH)
for i in range(1600):
    GPIO.output(stepPin, GPIO.HIGH)
    GPIO.output(stepPin, GPIO.LOW)
    wait(speed)

print("DONE")

    

