from threading import Thread
from time import sleep
import RPi.GPIO as GPIO

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)


first_pin = 11
second_pin = 13
third_pin = 15

def blink(pin):
    GPIO.setup(pin, GPIO.OUT)
    print("blinking")
    for i in range(20):
        GPIO.output(pin, GPIO.HIGH)
        sleep(.1)
        GPIO.output(pin, GPIO.LOW)
        sleep(.3)


def blink2(pin):
    GPIO.setup(pin, GPIO.OUT)
    print("blinking")
    for i in range(50):
        GPIO.output(pin, GPIO.HIGH)
        sleep(.1)
        GPIO.output(pin, GPIO.LOW)
        sleep(.1)


# blink(first_pin)
# blink(second_pin)
# blink(third_pin)


first_thread = Thread(target=blink, args=[first_pin])
second_thread = Thread(target=blink2, args=[second_pin])
third_thread = Thread(target=blink, args=[third_pin])

first_thread.start()
second_thread.start()
third_thread.start()

first_thread.join()
second_thread.join()
third_thread.join()


GPIO.cleanup()