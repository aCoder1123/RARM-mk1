from constants import *
from pinout import *

# GPIO = webiopi.GPIO



ROTATATIONAL_ANGLE = 0
BASE_ARM_ANGLE = 0
MID_ARM_ANGLE = 0
TOP_ARM_ANGLE = 0
HAND_ANGLE = 0
HAND_OPENESS = 1
HAND_POSITION = [0, 0, 0]



def point():
    pass

def getPosition() -> list:
    pass

def moveDirection(direction: list):
    pass


# c= sqrt a2+b2﹣2abcosγ

#cos^-1((c2-a2-b2)/-2ab) = theta

def getAngles(x: int, y: int, z: int) -> list:
    pass

