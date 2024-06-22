#importing webiopi for communication with web app and ServoArm class
import json
import StepperARM
import time

try: 
    import webiopi
    import RPi.GPIO as GPIO
except: print("Could not resolve imports.")

def wait(sleepTime: int) -> None:
        """ A function to precisly wait a given time in seconds."""
        initial = time.time()
        x = 1
        while time.time() - initial < sleepTime:
            x += 1

#initializing arm
RARM = StepperARM.StepperArm()
RARM.setup()

# macro to move arm to a given position 
@webiopi.macro
def arm_to_position(position: str):
    parsedPosition = position.split(";") #theta;radius;height
    finalPosition = [float(i) for i in parsedPosition]
    
    print("position is", finalPosition)
    try: 
        RARM.move_to_pos(finalPosition)
    except Exception as error:
        return error
    return "Command Sucessfully Executed"

@webiopi.macro
def test(led_pin= -1):
    
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(led_pin, GPIO.OUT)

        for i in range(10):
            GPIO.output(led_pin, GPIO.HIGH)
            time.sleep(.3)
            GPIO.output(led_pin, GPIO.LOW)
            time.sleep(.3)

        GPIO.output(13, GPIO.HIGH)
    except Exception as error:
        return f"Test Failed with error: {error}"
    # GPIO.cleanup()
    return "Test Successful"
    

@webiopi.macro
def set_setting(setting, value):
    settings = ["speed", ]
    val_to_set = value if setting != "speed" else value * 0.02
    
    if not setting in settings: return "Invalid Setting"
    with open("../../home/rarm-mk1/WebIOPi-0.7.1/htdocs/RARM-mk1/Python/config/settings.json") as f:
        data = json.load(f)
        data[setting] = val_to_set
        json.dump(data, f)
    
    RARM.settings[setting] = val_to_set
    
    return "Setting Set Successfully"

@webiopi.macro
def get_angles():
    return RARM.get_angles()

@webiopi.macro
def toggle():
    return RARM.toggle()

@webiopi.maccro
def move_stepper(stepperNum):
    start = time.time()
    
    pinDict = {}
    try:
        
        stepPin = 13
        dirPin = 21
        speed = 0.0015
        steps = 1000

        GPIO.setup(stepPin, GPIO.OUT)
        GPIO.setup(dirPin, GPIO.OUT)

        GPIO.output(dirPin, GPIO.LOW)
        for i in range(steps):
            GPIO.output(stepPin, GPIO.HIGH)
            GPIO.output(stepPin, GPIO.LOW)
            wait(speed)

        GPIO.output(dirPin, GPIO.HIGH)
        for i in range(steps) :
            GPIO.output(stepPin, GPIO.HIGH)
            GPIO.output(stepPin, GPIO.LOW)
            wait(speed)
           
    except Exception as error:
        return f"Test FAILED with error: {error}"
    
    return f"Test succesfully completed in {round(time.time() - start, 2)} seconds."