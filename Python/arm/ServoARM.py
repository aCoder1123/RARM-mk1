class ServoArm:
    #a class to contain almost the entire arm so the rest of the code can be cleaner and more readable
    def __init__(self, segmentLengths: list = [8.0, 8.0, 8.0]) -> None:
  
        #set up important variables and imports
        
        try: #try except statement so file with RPi exclusive imports still runs on mac
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


        #setting lengths of each segment of the arm for IKE
        self.BTM_LENGTH = segmentLengths[0]
        self.MID_LENGTH = segmentLengths[1]
        self.TOP_LENGTH = segmentLengths[2]
        self.TOTAL_LENGTH = self.BTM_LENGTH + self.MID_LENGTH + self.TOP_LENGTH

        self.ready = False


    def getAbsIKEAngles(self, pos: list = [0, 0, 20], noFlat = False) -> list:
        """Simple function for transalating desired position to arm andgles. Prioritizes the top segment being flat both as a matter of convinience and as a method for bringing it to one discrete solution when more than one is possible."""


        theta = pos[0]
        R = pos[1]
        H = pos[2]

        #handling for special cases
        switching = False
        if (R == 0 or R == 0.0) and (H == 8 or H == 8.0):
            baseAngle = 0
            midAngle = 90
            topAngle = 0
            return [baseAngle, midAngle, topAngle]
        elif (R == 8 or R == 8.0) and (H == 0 or H == 0.0):
            baseAngle = 90
            midAngle = 0
            topAngle = -90
            return [baseAngle, midAngle, topAngle]
        elif R == 0 or R == 0.0:
            switching = True
            R = pos[2]
            H = pos[1]
        
        #back to normal solving
        flat = (R - self.TOP_LENGTH)**2 + H**2 <= (self.MID_LENGTH + self.TOP_LENGTH)**2 #determines wether or not top can be flat


        baseAngle = None
        midAngle = None
        topAngle = None


        # if noFlat: flat = False

        #respective calculations for each possibility
        if flat:
            topAngle = 0
            if R == 8 or R == 8.0:
                tBM = 90
            else:
                tBM = self.M.degrees(self.M.atan(H/(R - self.TOP_LENGTH)))
            lBM = self.M.sqrt(H**2 + (R-self.TOP_LENGTH)**2)
            
            baseAngle = tBM + self.M.degrees(self.M.acos((self.BTM_LENGTH**2 + lBM**2 - self.MID_LENGTH**2)/(2*self.MID_LENGTH*lBM)))
            tBBM = baseAngle - tBM
            midAngle = tBM-tBBM

            if baseAngle < 0: 
                baseAngle +=180
                if midAngle < 0:
                    midAngle +=180
            if switching:
                baseAngle += 90
                midAngle += 90
                topAngle += 90
            
            
        else:
            lBM = self.BTM_LENGTH + self.TOP_LENGTH
            lBMT = self.M.sqrt(R**2 + H**2)
            tA = self.M.degrees(self.M.atan(H/R))
            tBM = self.M.degrees(self.M.acos((lBM**2 + lBMT**2 - self.TOP_LENGTH**2)/(2*lBM*lBMT))) + tA
            midAngle = baseAngle = tBM
            topAngle = tA - self.M.degrees(self.M.acos((self.TOP_LENGTH**2 + lBMT**2 - lBM**2)/(2*self.TOP_LENGTH*lBMT)))
            if switching:
                baseAngle += 90
                midAngle += 90
                topAngle += 90
                R = pos[1]
                H = pos[2]
        #readjusting for switched coordinants
        if ((baseAngle - midAngle) > 90) or ((midAngle - topAngle) > 90):      
                tBMT = self.M.degrees(self.M.atan(H/R))
                midAngle = tBMT
                lBMT = self.M.sqrt(H**2 + R**2)
                lBT = lBMT - self.MID_LENGTH
                baseAngle = tBMT+ self.M.degrees(self.M.acos((0.5 * lBT)/self.BTM_LENGTH))
                topAngle = (2*tBMT) - baseAngle

        return [baseAngle, midAngle, topAngle]


    class Joint:

        #basic class to package each joint into something addresable and easier to work with
        def __init__(self, pwmPin: int, ARM, dcMin: float, dcMax: float, straighAngle: float = 90.0, minAngle: int = 0, maxAngle: int = 180, invertDirection: int = 0) -> None:
            #setting constraints
            self. _maxAngle = maxAngle
            self._minAngle = minAngle
            self._straightAngle = straighAngle
            self._invertDirection = invertDirection

            self.ARM = ARM #passing arm joint belongs to


            #setting up servo communication and duty cycles for it
            self.pwmPin = pwmPin
            self.ARM.GPIO.setup(self.pwmPin, self.ARM.GPIO.OUT)
            self.dcMin = dcMin
            self.dcMax = dcMax
            self.servo = self.ARM.GPIO.PWM(self.pwmPin, 1000)
            self.servo.start(0)


                
        def turnToAngle(self, targetAngle, currentAngle = 0, wait: bool = True):
            #function to validate and execute changes to joint angle

            if targetAngle > self._maxAngle or targetAngle < self._minAngle: return

            dc = (self.dcMax-self.dcMin)*targetAngle/180 + self.dcMin #math to determine appropriate dc
            self.servo.ChangeDutyCycle(dc)
            if wait: #determines wether execution pauses to waut for the servo to reach the desired angle
                sleepTime = abs(targetAngle - currentAngle) /180
                self.ARM.T.sleep(sleepTime)
        def point(self, ) -> None:
            #function to straighten joint relative to previous one
            self.moveJoint(self.straightAngle)

    def getData(self, data: str = None) -> dict:
            #function to get and return optionally specified JSON data
           
            fPinouts = open(file="../../home/rarm-mk1/WebIOPi-0.7.1/htdocs/RARM-mk1/Python/config/servoData.json") 
            
            returnedData = self.load(fPinouts) #loads data
            fPinouts.close()
            if not data:
                return returnedData
            else:
                return returnedData[data]
    
    def setup(self, ):
        #function to start programatic setup of arm and joints
        data = self.getData()
        self.pins = data["sPins"]
        #initilizing joints and passing apropriate config data
        self.BottomJoint = self.Joint(self.pins["base"], self, data["dutyCycles"]["base"]["min"], data["dutyCycles"]["base"]["max"], data["angles"]["base"]["straight"], data["angles"]["base"]["min"], data["angles"]["base"]["max"], data["angles"]["base"]["inverted"])
        self.MidJoint = self.Joint(self.pins["mid"], self,  data["dutyCycles"]["mid"]["min"], data["dutyCycles"]["mid"]["max"], data["angles"]["mid"]["straight"], data["angles"]["mid"]["min"], data["angles"]["mid"]["max"], data["angles"]["mid"]["inverted"])
        self.TopJoint = self.Joint(self.pins["top"], self,  data["dutyCycles"]["top"]["min"], data["dutyCycles"]["top"]["max"], data["angles"]["top"]["straight"], data["angles"]["top"]["min"], data["angles"]["top"]["max"], data["angles"]["top"]["inverted"])
        
        self.point() #pointing at the end to indicate readiness
        self.ready = True
        
    def moveToAbsAngles(self, angles: list, pos: list,):
        #function to translate desired angles for the arm segments to servo positions to physical movements
        if not self.ready:
            print("Arm not initilized.")
            return
        self.pos = pos
        bAngle = angles[0]
        mAngle = angles[1]
        tAngle = angles[2]
        self.BottomJoint.turnToAngle(bAngle)
        self.MidJoint.turnToAngle(self.MidJoint._straightAngle-(bAngle-mAngle))
        self.TopJoint.turnToAngle(self.TopJoint._straightAngle-(mAngle-tAngle))

    def point(self, ) -> None:
        if not self.ready:
            print("Arm not initilized.")
            return

        #funtion to move arm to point straight up
        
        self.BottomJoint.point()
        self.MidJoint.point()
        self.TopJoint.point()
        self.pos = [0, 0, self.TOTAL_LENGTH]


    def kill(self, ) -> None:
        #function to stop servo communication and cleanup all gpio pins
        self.BottomJoint.servo.stop()
        self.MidJoint.servo.stop()
        self.TopJoint.servo.stop()
        self.GPIO.cleanup()

        self.ready = False
        

