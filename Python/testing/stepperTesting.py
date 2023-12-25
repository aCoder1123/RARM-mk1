import RPi.GPIO as GPIO
from miscTest import wait as wait
GPIO.setmode(GPIO.BOARD)

stepPin = 11
dirPin = 13
speed = 0.0002
steps = 3000

GPIO.setup(stepPin, GPIO.OUT)
GPIO.setup(dirPin, GPIO.OUT)

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
