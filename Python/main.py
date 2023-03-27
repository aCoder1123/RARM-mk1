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
    try: 
        if position: RARM.moveToAbsAngles(RARM.getAbsIKEAngles(position), position)
        else: RARM.kill()
    except Exception as error:
        return error
    return "Command Sucessfully Executed"

@webiopi.macro
def test():
    
    RARM.GPIO.setmode(RARM.GPIO.BOARD)
    RARM.GPIO.setup(13, RARM.GPIO.OUT)

    for i in range(10):
        RARM.GPIO.output(13, RARM.GPIO.HIGH)
        RARM.T.sleep(1)
        RARM.GPIO.output(13, RARM.GPIO.LOW)
        RARM.T.sleep(1)

    RARM.GPIO.output(13, RARM.GPIO.HIGH)

    RARM.GPIO.cleanup()
    return "Test Successful"
    