#importing webiopi for communication with web app and ServoArm class
import json
import StepperARM
import time

try: 
    import webiopi
    import RPi.GPIO as GPIO
except: print("Could not resolve imports.")

#initializing arm
RARM = StepperARM.StepperArm()
RARM.setup()

# macro to move arm to a given position 
@webiopi.macro
def arm_to_position(position: str):
    parsedPosition = position.split(";")
    finalPosition = [float(i) for i in parsedPosition]
    
    print("position is", finalPosition)
    try: 
        RARM.move_to_pos(finalPosition)
    except Exception as error:
        return error
    return "Command Sucessfully Executed"

@webiopi.macro
def test(led_pin= 13):
    
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