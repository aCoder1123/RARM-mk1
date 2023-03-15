from constants import *
from time import sleep
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT) 
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.HIGH)
x =1
for i in range(0, 10000): 
            print(x)
            x+=1
            GPIO.output(3, (GPIO.HIGH))
            sleep(0.04)
            GPIO.output(3, (GPIO.LOW))
            sleep(0.04)
print("stopping")
GPIO.cleanup()

# print(time.time())