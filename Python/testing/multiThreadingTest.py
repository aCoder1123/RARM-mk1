from threading import Thread
from time import sleep
import RPi.GPIO as GPIO

def blink(pin):
    for i in range(100):
        

GPIO.setmode(GPIO.BCM)
