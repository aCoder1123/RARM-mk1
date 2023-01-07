from constants import *
GPIO.setmode(GPIO.BOARD)


test = Joint([3, 5, 100])

print('starting')

test.moveJoint(0, 1, 100)
test.moveJoint(1, 1, 100)
