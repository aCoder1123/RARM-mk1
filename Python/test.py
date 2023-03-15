from constants import *
GPIO.setmode(GPIO.BOARD)


test = Joint([3, 5, 7])
print(1)
wait(100)
print(2)
print('starting')

test.angle = 100
test.moveJoint(0, 1, 100)
test.moveJoint(1, 1, 100)

print("stopping")
GPIO.cleanup()