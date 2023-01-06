from constants import *
from pinout import *

# GPIO = webiopi.GPIO



ROTATATIONAL_ANGLE = 0
BASE_ANGLE = 0
MID_ANGLE = 0
TOP_ANGLE = 0
HAND_ANGLE = 0
HAND_OPENESS = 1
HAND_POSITION = [0, 0, 0]



def point():
    pass

def getPosition() -> list:
    pass

def moveDirection(direction: list):
    pass



def getAngles(x: int, y: int, z: int) -> list:
    base = m.degrees(m.atan(y/x))
    xyDistance = m.sqrt((x**2 + y**2))
    xyJ3 = xyDistance - TOP_LENGTH
    if (MID_LENGTH) :
        pass
    




