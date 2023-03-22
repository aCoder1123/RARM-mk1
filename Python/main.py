from ARM import ServoArm
try: import webiopi
except: print("couldn't resolve imports")

RARM = ServoArm()
RARM.setup()


@webiopi.macro
def moveToPosition(position: list):
    RARM.moveToAbsAngles(RARM.getAbsIKEAngles(position), position)