from ARM import ServoArm
import math
from random import randint
import traceback


test = ServoArm

test.__init__(test)

errors = False

for i in range(1, 6000001):
    if i % 200000 == 0.0:
        print("Test: "+ str(i))
    try: 
        a = 0
        b = randint(0,2400)/100
        c = randint(0, 2400)/100
        while math.sqrt(b**2 + c**2) > 24:
            b = randint(0,2400)/100
            c = randint(0, 2400)/100
        
        test.getAbsIKEAngles(test, pos=[a,b,c])
    except Exception as error:
        errors =True
        print(i)
        print(f"\nFailed:\n{a}\n{b}\n{c}\n{error}\n")
        traceback.print_tb(error.__traceback__)
        print("\n")


if not errors:
    print("\nAll tests passed without errors.")

