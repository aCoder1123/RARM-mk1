import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
            
GPIO.setup(7, GPIO.OUT)

for i in range(10):
    GPIO.output(7, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(7, GPIO.LOW)
    time.sleep(1)

GPIO.output(7, GPIO.HIGH)

GPIO.cleanup()