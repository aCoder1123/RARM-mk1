class ServoArm:
    def __init__(self, segmentLengths: list = [8.0, 8.0, 8.0]) -> None:
  
        try: 
            import RPi.GPIO
            self.GPIO = RPi.GPIO
            self.GPIO.setmode(self.GPIO.BOARD)
        except: print("Couldn't resolve imports.")
        import time 
        self.T = time
        import math
        self.M = math
        from json import load
        from os import getcwd
        self.load = load
        self.getcwd = getcwd

        self.BTM_LENGTH = segmentLengths[0]
        self.MID_LENGTH = segmentLengths[1]
        self.TOP_LENGTH = segmentLengths[2]
        self.TOTAL_LENGTH = self.BTM_LENGTH + self.MID_LENGTH + self.TOP_LENGTH
        self.point()

        self.pos = [0, 0, self.TOTAL_LENGTH]

    def getAbsIKEAngles(self, pos: list = [0, 0, 20]) -> list:
        theta = pos[0]
        R = pos[1]
        H = pos[2]
        flat = (R - self.TOP_LENGTH)**2 + H**2 <= (self.MID_LENGTH + self.TOP_LENGTH)**2


        baseAngle = None
        midAngle = None
        topAngle = None
        if flat:
            topAngle = 0
            tBM = self.M.atan(H/(R - self.TOP_LENGTH))
            lBM = self.M.sqrt(H**2 + (R-self.TOP_LENGTH)**2)
            baseAngle = tBM + self.M.acos((self.BTM_LENGTH**2 + lBM**2 - self.MID_LENGTH)/(2*self.MID_LENGTH*lBM))
            tBBM = baseAngle - tBM
            midAngle = tBM-tBBM
        else:
            lBM = self.BTM_LENGTH + self.TOP_LENGTH
            lBMT = self.M.sqrt(R**2 + H**2)
            tA = self.M.atan(H/R)
            tBM = self.M.acos((lBM**2 + lBMT**2 - self.TOP_LENGTH**2)/(2*lBM*lBMT)) + tA
            midAngle = topAngle = tBM
            topAngle = tA - self.M.acos((self.TOP_LENGTH**2 + lBMT**2 - lBM**2)/2*self.TOP_LENGTH*lBMT)
        
        return [baseAngle, midAngle, topAngle]

    class Joint:
        def __init__(self, pwmPin: int, ARM, dcMin: float, dcMax: float, straighAngle: float = 90.0, minAngle: int = 0, maxAngle: int = 180, invertDirection: int = 0) -> None:
            self. _maxAngle = maxAngle
            self._minAngle = minAngle
            self._straightAngle = straighAngle
            
            
            self._invertDirection = invertDirection

            self.pwmPin = pwmPin
            self.dcMin = dcMin
            self.dcMax = dcMax
            

            self.ARM = ARM
            self.servo = ARM.GPIO.PWM(self.pwmPin, 1000)
            self.servo.start(0)
                
        def turnToAngle(self, targetAngle, currentAngle):
            dc = (self.dcMax-self.dcMin)*targetAngle/180 + self.dcMin
            self.servo.ChangeDutyCycle(dc)
            sleepTime = abs(targetAngle - currentAngle) /180
            self.sleep(sleepTime)
        def point(self, ) -> None:
            self.moveJoint(self.straightAngle)

    def getData(self, data: str = None) -> dict:
            if str(self.getcwd())[-6:len(str(self.getcwd()))] == "Python":
                fPinouts = open(file="config/servoData.json") 
            else:
                fPinouts = open(file="Python/config/servoData.json")
            pins = self.load(fPinouts)
            fPinouts.close()
            if not data:
                return pins
            else:
                return pins[data]
    
    def setup(self, ):
        data = self.getData()
        self.pins = data["sPins"]
        self.BottomJoint = self.Joint(self.pins["base"], self, data["dutyCycles"]["base"]["min"], data["dutyCycles"]["base"]["max"], data["angles"]["base"]["straight"], data["angles"]["base"]["min"], data["angles"]["base"]["max"], data["angles"]["base"]["inverted"])
        self.MidJoint = self.Joint(self.pins["mid"], self,  data["dutyCycles"]["mid"]["min"], data["dutyCycles"]["mid"]["max"], data["angles"]["mid"]["straight"], data["angles"]["mid"]["min"], data["angles"]["mid"]["max"], data["angles"]["mid"]["inverted"])
        self.TopJoint = self.Joint(self.pins["top"], self,  data["dutyCycles"]["top"]["min"], data["dutyCycles"]["top"]["max"], data["angles"]["top"]["straight"], data["angles"]["top"]["min"], data["angles"]["top"]["max"], data["angles"]["top"]["inverted"])
        
        self.point()

    def moveToAbsAngles(self, angles: list, pos: list,):
        self.pos = pos
        bAngle = angles[0]
        mAngle = angles[1]
        tAngle = angles[2]
        self.BottomJoint.turnToAngle(bAngle)
        self.MidJoint.turnToAngle(self.MidJoint._straightAngle-(bAngle-mAngle))
        self.TopJoint.turnToAngle(self.TopJoint._straightAngle-(mAngle-tAngle))

    def point(self, ) -> None:
        self.BottomJoint.point()
        self.MidJoint.point()
        self.TopJoint.point()

    def kill(self, ) -> None:
        self.BottomJoint.servo.stop()
        self.MidJoint.servo.stop()
        self.TopJoint.servo.stop()
        self.GPIO.cleanup()


# class stepperARM:
#     def __init__(self, pulseDelay: float = 0.02, segmentLengths: list = [8.0, 8.0, 8.0]) -> None:
  
#         try: 
#             import RPi.GPIO
#             self.GPIO = RPi.GPIO
#         except: pass
#         import time 
#         self.T = time
#         import math
#         self.M = math

#         self.pulseDelay = pulseDelay
#         self.BTM_LENGTH = segmentLengths[0]
#         self.MID_LENGTH = segmentLengths[1]
#         self.TOP_LENGTH = segmentLengths[2]
#         self.TOTAL_LENGTH = self.BTM_LENGTH + self.MID_LENGTH + self.TOP_LENGTH
#         self.point()

#         self.pos = [0, 0, self.TOTAL_LENGTH]

#     def getPosition(self, ) -> list:
#         return self.pos


#     def wait(self, sleepTime: int) -> None:
#         initial = self.T.time()
#         x = 1
#         while self.T.time() - initial < sleepTime:
#             x += 1

#     def getAbsIKEAngles(self, pos: list = [0, 0, 20]) -> list:
#         theta = pos[0]
#         R = pos[1]
#         H = pos[2]
#         flat = (R - self.TOP_LENGTH)**2 + H**2 <= (self.MID_LENGTH + self.TOP_LENGTH)**2


#         baseAngle = None
#         midAngle = None
#         topAngle = None
#         if flat:
#             topAngle = 0
#             tBM = self.M.atan(H/(R - self.TOP_LENGTH))
#             lBM = self.M.sqrt(H**2 + (R-self.TOP_LENGTH)**2)
#             baseAngle = tBM + self.M.acos((self.BTM_LENGTH**2 + lBM**2 - self.MID_LENGTH)/(2*self.MID_LENGTH*lBM))
#             tBBM = baseAngle - tBM
#             midAngle = tBM-tBBM
#         else:
#             lBM = self.BTM_LENGTH + self.TOP_LENGTH
#             lBMT = self.M.sqrt(R**2 + H**2)
#             tA = self.M.atan(H/R)
#             tBM = self.M.acos((lBM**2 + lBMT**2 - self.TOP_LENGTH**2)/(2*lBM*lBMT)) + tA
#             midAngle = topAngle = tBM
#             topAngle = tA - self.M.acos((self.TOP_LENGTH**2 + lBMT**2 - lBM**2)/2*self.TOP_LENGTH*lBMT)
        
#         return [baseAngle, midAngle, topAngle]


#     class Joint:
#         def __init__(self, pins: list, ARM, maxAngle: int = 180, name: str = '', SPR: int = 600, invertDirection: int = 0) -> None:
#             self. _maxAngle = maxAngle
#             self.angle = None
#             self._invertDirection = invertDirection
            
#             self._pins = {'step': pins[0], 'dir': pins[1], 'zero': pins[2]}
#             self.GPIO.setup(self._pins['step'], self.GPIO.OUT)
#             self.GPIO.setup(self._pins['dir'], self.GPIO.OUT)
#             self.GPIO.setup(self._pins['zero'], self.GPIO.IN)
            
#             self._SPR = SPR

#             self.name = name
#             self._atZero = False
#             self.ARM = ARM
        
#         def __repr__(self) -> str:
#             return f"Joint: name = {self.name}, step: {self._pins['step']}, dir: {self._pins['dir']}, zero: {self._pins['zero']}, sweep: {self._sweep}, SPR: {self._SPR}"

#         def moveJoint(self, direction: int = 0, delay = 0.02, steps = 1) -> None:
#             # if (not direction and self.angle >= 0) or (direction and self.angle <= self._maxAngle): 
#             #     print("returning")
#             #     return
#             if (direction and not self._invertDirection) or (not direction and self._invertDirection):
#                 self.GPIO.output(self._pins['dir'], self.GPIO.HIGH)
#             else: self.GPIO.output(self._pins['dir'], self.GPIO.LOW)

#             for i in range(0, steps): 
#                 print("moving")
#                 self.GPIO.output(self._pins['step'], self.GPIO.HIGH)
#                 self.wait(delay)
#                 self.GPIO.output(self._pins['step'], self.GPIO.LOW)
#                 self.wait(delay)



#         def zero(self) -> None:
#             if self._atZero: return
#             while not self.GPIO.input():
#                 if self._zeroPos > 0: self.moveJoint(1)
#                 else: self.moveJoint()
#             self._atZero = True
#             self.angle = self._zeroPos

    
#     def setup(self, ):
#         BottomJoint = self.Joint()
        

#     def moveToAbsAngles(self, angles: list, pos: list,):
#             self.pos = pos

    
#         return

#     def point(self, ):
#         self.moveToAbsAngles([90, 90, 90])


