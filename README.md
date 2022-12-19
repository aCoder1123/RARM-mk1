# RARM-mk1

## WepIoPi web app and inverse kinematics for controlling the RARM mk1

A robotic arm controlled by six stepper motors and controlled from your computer. The **PI** is running a **WebIoPi** server that then runs macros on the **PI**. The **PI** calculates inverse kinematics and then uses **TMC2208** stepper drivers to drive the **FYSETC** stepper motors.

```py
class Joint: 
        def __init__ (self):
            pass
        def __repr__(self):
            pass
        def moveJoint(self):
            pass
        def zero(self):
            pass

```
