#importing webiopi for communication with web app and ServoArm class

from ARM import ServoArm
try: import webiopi
except: print("couldn't resolve imports")


#initializing arm
RARM = ServoArm()
RARM.setup()


# macro to move arm to a given position 
@webiopi.macro
def moveToPosition(position: list):
    RARM.moveToAbsAngles(RARM.getAbsIKEAngles(position), position)