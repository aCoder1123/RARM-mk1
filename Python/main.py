from functions import *


SmoothingConstant = 1

GPIO.setmode(GPIO.BOARD)


@webiopi.macro
def moveToPosition(position: list):
    angles = getAngles(position[0], position[1], position[2])
    for i in range():
        pass

@webiopi.macro
def getStatus() -> str:
    pass

@webiopi.macro
def settingSet():
    pass









GPIO.cleanup()