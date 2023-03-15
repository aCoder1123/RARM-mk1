import RPIO
import time

RPIO.setmode(RPIO.BOARD)
            
RPIO.setup(7, RPIO.OUT)

for i in range(10):
    RPIO.output(7, RPIO.HIGH)
    time.sleep(1)
    RPIO.output(7, RPIO.LOW)
    time.sleep(1)

RPIO.output(7, RPIO.HIGH)

RPIO.cleanup()