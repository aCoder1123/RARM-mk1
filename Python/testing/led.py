"""
Preliminary test file to try to use the GPIO pins in the simplest form
just turns on and off an led on pin 13

"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
            
GPIO.setup(13, GPIO.OUT)

for i in range(10):
    GPIO.output(13, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(13, GPIO.LOW)
    time.sleep(1)

GPIO.output(13, GPIO.HIGH)

GPIO.cleanup()