from functions import *

SmoothingConstant = 1

GPIO.setmode(GPIO.BOARD)


baseJoint = Joint([sPins['base'], dPins['base'], zPins['base']], None)
lowerJoint = Joint([sPins['lower'], dPins['lower'], zPins['lower']])
midJoint = Joint([sPins['mid'], dPins['mid'], zPins['mid']])
highJoint = Joint([sPins['high'], dPins['high'], zPins['high']])
rotaryJoint = Joint([sPins['rotary'], dPins['rotary'], zPins['rotary']], None)
actuatorJoint = Joint([sPins['actuator'], dPins['actuator'], zPins['actuator']])


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