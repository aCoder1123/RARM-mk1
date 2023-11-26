import RPi.GPIO as GPIO
from miscTest import wait as wait
GPIO.setmode(GPIO.BCM)

stepPin = 15
dirPin = 22
speed = 0.01

GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

print(1)
GPIO.output(dirPin, GPIO.LOW)
for i in range(400):
    GPIO.output(stepPin, GPIO.HIGH)
    wait(speed)
    GPIO.output(stepPin, GPIO.LOW)
    wait(speed)

print(2)
GPIO.output(dirPin, GPIO.HIGH)
for i in range(400):
    GPIO.output(stepPin, GPIO.HIGH)
    GPIO.output(stepPin, GPIO.LOW)
    wait(speed)

print("DONE")

    
GPIO.cleanup()
