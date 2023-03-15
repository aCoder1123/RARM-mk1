import math as m
import time
import RPi.GPIO as GPIO

BASE_LENGTH = 1
MID_LENGTH = 1
TOP_LENGTH = 1
MIN_SPEED = 100


def wait(timeNs):
    initial = time.time()
    while time.time() - initial < 5:#(timeNs / 1000):
        x=1


class Joint:
    def __init__(self, pins: list, maxAngle: int = 180, name: str = '', SPR: int = 600, invertDirection: int = 0,) -> None:
        self. _maxAngle = maxAngle
        self.angle = None
        self._invertDirection = invertDirection
        
        self._pins = {'step': pins[0], 'dir': pins[1], 'zero': pins[2]}
        GPIO.setup(self._pins['step'], GPIO.OUT)
        GPIO.setup(self._pins['dir'], GPIO.OUT)
        GPIO.setup(self._pins['zero'], GPIO.IN)
        
        self._SPR = SPR

        self.name = name
        self._atZero = False
    
    def __repr__(self) -> str:
        return f"Joint: name = {self.name}, step: {self._pins['step']}, dir: {self._pins['dir']}, zero: {self._pins['zero']}, sweep: {self._sweep}, SPR: {self._SPR}"

    def moveJoint(self, direction: int = 0, speed = 1, steps = 1) -> None:
        # if (not direction and self.angle >= 0) or (direction and self.angle <= self._maxAngle): 
        #     print("returning")
        #     return
        if (direction and not self._invertDirection) or (not direction and self._invertDirection):
            GPIO.output(self._pins['dir'], GPIO.HIGH)
        else: GPIO.output(self._pins['dir'], GPIO.HIGH)

        for i in range(0, steps): 
            print("moving")
            GPIO.output(self._pins['step'], GPIO.HIGH)
            wait(MIN_SPEED)
            GPIO.output(self._pins['step'], GPIO.LOW)
            wait(MIN_SPEED)



    def zero(self) -> None:
        if self._atZero: return
        while not GPIO.input():
            if self._zeroPos > 0: self.moveJoint(1)
            else: self.moveJoint()
        self._atZero = True
        self.angle = self._zeroPos


