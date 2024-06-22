import math
import threading
import time
from json import load

from serial_coms import read_pin, set_serial

try: #try except statement so file with RPi exclusive imports still runs on mac
    import RPi.GPIO as GPIO
except: print("Could not resolve imports.")


# todo base cad
# todo angles
# todo settings / console

# todo linefollowing
# TODO Comments/descriptions
# todo better readme / logo


class StepperArm:
    #a class to contain almost the entire arm so the rest of the code can be cleaner and more readable

    def __init__(self, segment_length: int = 150) -> None:
    
        #setting lengths of each segment of the arm for IKE
        self.segment_length = segment_length
        
        self.TOP_LENGTH = self.segment_length
        self.MID_LENGTH = self.segment_length
        self.BTM_LENGTH = self.segment_length

        self.ready = False
        self.enabled = False
        
        self.joint_gearing = 45/10
        
    def getAbsIKEAngles(self, pos: list = [0, 0, 450]) -> list[float]:
        """Simple function for transalating desired position to arm andgles. Prioritizes the top segment being flat both as a matter of convinience and as a method for bringing it to one discrete solution when more than one is possible."""


        theta = pos[0]
        R = pos[1]
        H = pos[2]

        #handling for special cases
        switching = False
        if (R == 0) and (H == self.segment_length):
            baseAngle = 0
            midAngle = 90
            topAngle = 0
            return [baseAngle, midAngle, topAngle]
        elif (R == 8) and (H == 0):
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
            if R == self.segment_length:
                tBM = 90
            else:
                tBM = math.degrees(math.atan(H/(R - self.TOP_LENGTH)))
            lBM = math.sqrt(H**2 + (R-self.TOP_LENGTH)**2)
            
            baseAngle = tBM + math.degrees(math.acos((self.BTM_LENGTH**2 + lBM**2 - self.MID_LENGTH**2)/(2*self.MID_LENGTH*lBM)))
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
            lBMT = math.sqrt(R**2 + H**2)
            tA = math.degrees(math.atan(H/R))
            tBM = math.degrees(math.acos((lBM**2 + lBMT**2 - self.TOP_LENGTH**2)/(2*lBM*lBMT))) + tA
            midAngle = baseAngle = tBM
            topAngle = tA - math.degrees(math.acos((self.TOP_LENGTH**2 + lBMT**2 - lBM**2)/(2*self.TOP_LENGTH*lBMT)))
            if switching:
                baseAngle += 90
                midAngle += 90
                topAngle += 90
                R = pos[1]
                H = pos[2]
        #readjusting for switched coordinants
        if ((baseAngle - midAngle) > 90) or ((midAngle - topAngle) > 90):      
                tBMT = math.degrees(math.atan(H/R))
                midAngle = tBMT
                lBMT = math.sqrt(H**2 + R**2)
                lBT = lBMT - self.MID_LENGTH
                baseAngle = tBMT+ math.degrees(math.acos((0.5 * lBT)/self.BTM_LENGTH))
                topAngle = (2*tBMT) - baseAngle

        return [baseAngle, midAngle, topAngle, theta]

    def getData(self, data: str = None) -> dict:
            """gets and returns specified JSON data"""
           
            fPinouts = open(file="../../home/rarm-mk1/WebIOPi-0.7.1/htdocs/RARM-mk1/Python/config/stepperData.json") 
            
            loaded_data = load(fPinouts)
            fPinouts.close()
            
            return loaded_data[data] if data else loaded_data
    
    def setup(self, ) -> None:
        """starts programatic setup of arm, joints, and GPIO pins"""
        data = self.getData()
        self.config = data
        self.settings = data["settings"]
        
        self.enable_pin = data["e_pin"]
        self.test_pin = data["test_pin"]
        
        self.serial_conn = set_serial()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.test_pin, GPIO.LOW)
        GPIO.setup(self.enable_pin, GPIO.HIGH)
        # GPIO.output(self.enable_pin, GPIO.LOW)
        GPIO.output(self.test_pin, GPIO.HIGH)
        #initilizing joints and passing apropriate config data
        self.ArmBase = self.Base(self, data["base"])
        self.BottomJoint = self.Joint(self, data["lower"])
        self.MidJoint = self.Joint(self, data["mid"])
        self.TopJoint = self.Joint(self, data["high"])
        
        self.point() #pointing at the end to indicate readiness
        
        self.ready = True
        
    def move_to_angles(self, angles: list,):
        """moves arm to given angles"""
        if not self.ready:
            print("Arm not initilized.")
            return
        elif not self.enabled:
            print("Arm not Enabled.")
            return
        
        b_angle = angles[3]
        l_angle = angles[0]
        m_angle = angles[1]
        t_angle = angles[2]
        
        base_thread = threading.Thread(target=self.BottomJoint.turn_to_angle_dr, args=(b_angle))
        lower_thread = threading.Thread(target=self.BottomJoint.turn_to_angle_dr, args=(l_angle))
        middle_thread = threading.Thread(target=self.MidJoint.turn_to_angle_dr, args=(self.MidJoint.straight_angle-(l_angle-m_angle)))
        top_thread = threading.Thread(target=self.TopJoint.turn_to_angle_dr, args=(self.TopJoint.straight_angle-(m_angle-t_angle)))
        
        base_thread.start()
        lower_thread.start()
        middle_thread.start()
        top_thread.start()
        
        base_thread.join()
        lower_thread.join()
        middle_thread.join()
        top_thread.join()
        
    def move_to_pos(self, pos: list,):
        """moves arm to given position"""
        if not self.ready:
            print("Arm not initilized.")
            return
        elif not self.enabled:
            print("Arm not Enabled.")
            return
        
        pos_angles = self.getAbsIKEAngles(pos)
        self.move_to_angles(pos_angles)
        
        self.pos = pos

    def point(self, ) -> None:
        """Funtion to move arm to point straight up."""

        if not self.ready:
            print("Arm not initilized.")
            return
        elif not self.enabled:
            print("Arm not Enabled.")
            return
        
        self.BottomJoint.point()
        self.MidJoint.point()
        self.TopJoint.point()
        self.pos = [0, 0, self.TOTAL_LENGTH]
    
    def get_angles(self) -> list[int]:
        return [self.BottomJoint.get_angle(), self.MidJoint.get_angle(), self.TopJoint.get_angle(), self.ArmBase.get_angle()]
    
    def toggle(self):
        if self.enabled:
            self.enabled = False
            GPIO.output(self.enable_pin, GPIO.HIGH)
            return "ARM Disabled."
        else:
            self.enabled = True
            GPIO.output(self.enable_pin, GPIO.LOW)
            return "ARM Enabled."
            
    
    def kill(self, ) -> None:
        """function to stop stepper communication and cleanup all gpio pins"""
        GPIO.output(self.enable_pin, GPIO.HIGH)
        self.ready = False
        GPIO.cleanup()
        read_pin(-1, self.serial_conn)
    
    
    class Joint:
        """Class to package each joint into something addresable and easier to work with"""
        def __init__(self, arm, data_dict: dict, gearing: float = (45/20)) -> None:
            
            self.max_sweep = data_dict["max"]
            self.straight_val = data_dict["straight"]
            self._invertDirection = data_dict["inverted"]
            self.speed = data_dict["speed"]
            self.pins = {'step': data_dict["sPin"], 'dir': data_dict["dPin"], 'pot': data_dict["potPin"]}
            
            self.angle = None #self.get_angle()
            self.straight_angle = self.straight_val/1023 * self.max_sweep
            self.parent_arm = arm
            self.spr = 200 * gearing 
            """motor steps per segment rotation"""
            
            GPIO.setup(self.pins['step'], GPIO.OUT)
            GPIO.setup(self.pins['dir'], GPIO.OUT)

                
        def __repr__(self) -> str:
            return f"Joint: step: {self.pins['step']}, dir: {self.pins['dir']} at angle: {round(self.get_angle())}"

        def get_angle(self) -> float:
            reading = read_pin(self.pins['pot'], self.parent_arm.serial_conn)
            return ((reading - self.straight_val)/1023) * self.max_sweep
        
        def move_joint(self, direction: int = 0, speed_mult:float = 1.0, steps = 1) -> None:
            if (direction and not self._invertDirection) or (not direction and self._invertDirection):
                GPIO.output(self.pins['dir'], GPIO.HIGH)
            else: GPIO.output(self.pins['dir'], GPIO.LOW)

            for i in range(0, steps): 
                print("moving")
                GPIO.output(self.pins['step'], GPIO.HIGH)
                self.wait(self.speed * (1/speed_mult))
                GPIO.output(self.pins['step'], GPIO.LOW)
                self.wait(self.speed * (1/speed_mult))
        
        def turn_to_angle_dr(self, ang, speed_mult:float = 1.0,):
            
            if ang < 0 or ang > self.max_sweep: 
                raise ValueError("Invalid Angle")
            
            steps = abs((ang-self.angle)/360 * self.spr)
            if ((ang-self.angle > 0) and not self._invertDirection) or (not (ang-self.angle > 0) and self._invertDirection):
                GPIO.output(self.pins['dir'], GPIO.HIGH)
            else: GPIO.output(self.pins['dir'], GPIO.LOW)
            
            for i in range(steps):
                GPIO.output(self.pins['step'], GPIO.HIGH)
                GPIO.output(self.pins['step'], GPIO.LOW)
                self.wait(self.speed * (1/speed_mult))
            
            return self.angle
        
        def turn_to_angle_fb(self, ang, speed_mult:float = 1.0,):
            if ang < 0 or ang > self.max_sweep: 
                raise ValueError("Invalid Angle")
            
            self.angle = self.read_angle()
            steps = abs((ang-self.angle)/360 * self.spr)
            if ((ang-self.angle > 0) and not self._invertDirection) or (not (ang-self.angle > 0) and self._invertDirection):
                GPIO.output(self.pins['dir'], GPIO.HIGH)
            else: GPIO.output(self.pins['dir'], GPIO.LOW)
            
            for i in range(steps):
                GPIO.output(self.pins['step'], GPIO.HIGH)
                GPIO.output(self.pins['step'], GPIO.LOW)
                self.wait(self.speed * (1/speed_mult))
            
            for i in range(5):
                self.angle = self.read_angle()
                if abs(self.angle - ang) < 3: break
                steps = abs((ang-self.angle)/360 * self.spr)
                if ((ang-self.angle > 0) and not self._invertDirection) or (not (ang-self.angle > 0) and self._invertDirection):
                    GPIO.output(self.pins['dir'], GPIO.HIGH)
                else: GPIO.output(self.pins['dir'], GPIO.LOW)
                
                for i in range(steps):
                    GPIO.output(self.pins['step'], GPIO.HIGH)
                    GPIO.output(self.pins['step'], GPIO.LOW)
                    self.wait(self.speed * (1/speed_mult))
            
            if abs(self.angle - ang) > 3: 
                return False
            return self.angle
        
        def point(self, ) -> None:
            #function to straighten joint relative to previous one
            self.turn_to_angle_dr(self.straightAngle)
            
        def zero(self) -> None:
            if abs(self.angle) < 1: return
            self.turn_to_angle_dr(0)
            
        def wait(self, sleepTime: int) -> None:
            initial = time.time()
            x = 1
            while time.time() - initial < sleepTime:
                x += 1

    class Base:
        """Class to package each joint into something addresable and easier to work with"""
        def __init__(self, arm, data_dict: dict, gearing: float = (200/20)) -> None:
            
            self.angle = None
            self._invertDirection = data_dict["inverted"]
            self.speed = data_dict["speed"]
            self.pins = {'step': data_dict["sPin"], 'dir': data_dict["dPin"], "pot": data_dict["z_pin"]}
            
            GPIO.setup(self.pins['step'], GPIO.OUT)
            GPIO.setup(self.pins['dir'], GPIO.OUT)
 
            self.parent_arm = arm
            self.spr = 200 * gearing 
            """motor steps per segment rotation"""
            
            self.zero()

        def get_angle(self) -> float:
            return self.angle
        
        def move_base(self, direction: int = 0, speed_mult:float = 1.0, steps = 1) -> None:
            if (direction and not self._invertDirection) or (not direction and self._invertDirection):
                GPIO.output(self.pins['dir'], GPIO.HIGH)
            else: GPIO.output(self.pins['dir'], GPIO.LOW)

            for i in range(0, steps): 
                print("moving")
                GPIO.output(self.pins['step'], GPIO.HIGH)
                GPIO.output(self.pins['step'], GPIO.LOW)
                self.wait(self.speed * (1/speed_mult))
        
        def turn_to_angle(self, ang, speed_mult:float = 1.0):
            
            angle = ang%360
            angle = angle if angle >= 0 else angle + 360
            
            differance, direction = angle - self.angle, True if angle - self.angle <= 180 else self.angle - angle, False
            direction = not direction if self._invertDirection else direction
            steps = abs(differance/360 * self.spr)
            if ((ang-self.angle > 0) and not self._invertDirection) or (not (ang-self.angle > 0) and self._invertDirection):
                GPIO.output(self.pins['dir'], GPIO.HIGH)
            else: GPIO.output(self.pins['dir'], GPIO.LOW)
            
            for i in range(steps):
                GPIO.output(self.pins['step'], GPIO.HIGH)
                GPIO.output(self.pins['step'], GPIO.LOW)
                self.wait(self.speed * (1/speed_mult))
            
            return self.angle
        
        def point(self, ) -> None:
            #function to straighten joint relative to previous one
            self.zero()
            
        def zero(self, speed_mult: float = 1.0) -> None:
            """finds and goes to zero position"""
            
            direction = GPIO.HIGH if self.angle and (self.angle > 180) else GPIO.LOW
            direction = not direction if self._invertDirection else direction
            
            while GPIO.input(self.pins["pot"]) > 10:
                GPIO.output(self.pins['step'], GPIO.HIGH)
                GPIO.output(self.pins['step'], GPIO.LOW)
                self.wait(self.speed * (1/speed_mult))
            
            self.angle = 0
            
        def wait(self, wait_time: int ) -> None:
            """Waits for given time (seconds)."""
            initial = time.time()
            x = 1
            while time.time() - initial < wait_time:
                x += 1
        
