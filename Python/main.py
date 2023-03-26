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
    if position: RARM.moveToAbsAngles(RARM.getAbsIKEAngles(position), position)
    else: RARM.kill()

@webiopi.macro
def test():

    RARM.GPIO.setmode(RARM.GPIO.BOARD)
                
    RARM.GPIO.setup(7, RARM.GPIO.OUT)

    for i in range(10):
        RARM.GPIO.output(7, RARM.GPIO.HIGH)
        RARM.T.sleep(1)
        RARM.GPIO.output(7, RARM.GPIO.LOW)
        RARM.T.sleep(1)

    RARM.GPIO.output(7, RARM.GPIO.HIGH)

    RARM.GPIO.cleanup()
    