from StepperARM import StepperArm
import math
from random import randint
import traceback


test = StepperArm()

mode = input("Enter mode: ")

if mode == "t": 
    errors = False

    for i in range(1, 6000000):
        if i % 200000 == 0.0:
            print("Test: "+ str(i))

        try: 
            a = 0
            b = randint(0,2400)/100
            c = randint(0, 2400)/100
            while math.sqrt(b**2 + c**2) > 12 or math.sqrt(b**2 + c**2) < 8:
                b = randint(0,2400)/100
                c = randint(0, 2400)/100
            
            angles = test.getAbsIKEAngles(test, pos=[a,b,c])
            if angles[0] < 0:
                raise ValueError
            # if ((angles[0] - angles[1]) > 90) or ((angles[1] - angles[2]) > 90):
            #      raise ValueError
        except Exception as error:
            errors =True
            print(i)
            print(f"\nFailed:\n{a}\n{b}\n{c}\n{error}\nAngles: {angles}\n")
            traceback.print_tb(error.__traceback__)
            print("\n")

    


    if not errors:
        print("\nAll tests passed without errors.")

else: 
    position = [float(i)  for i in input("Enter Pos:").split(",")]
    while position:
        angles = test.getAbsIKEAngles(position)
        print(angles)
        position = [float(i)  for i in input("Enter Pos:").split(",")]
        
        
