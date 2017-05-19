# -------------------------------------------------- # 
# ---  Library : Board Library --------------------- #
# -------------------------------------------------- #


# -------------------------------------------------- # 
# ---  Import Modules  ----------------------------- #
# -------------------------------------------------- #
import random
import time
import math
import threading
from pyBBBDrone import *
# -------------------------------------------------- #



# -------------------------------------------------- # 
# ---  Global Variables  --------------------------- #
# -------------------------------------------------- #
global Pitch
global Roll
global Yaw
Pitch = 0.0
Roll = 0.0
Yaw = 0.0
# -------------------------------------------------- #





# -------------------------------------------------- # 
# ---  Threads   ----------------------------------- #
# -------------------------------------------------- #
class ThreadIMU (threading.Thread):
    def __init__(self, threadID, name,IMUData):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global Pitch
        global Roll
        global Yaw
        while True:
            if IMUData.IMURead():
                x, y, z = IMUData.getFusionData()
                Pitch = math.degrees(x - Pitch0) -3
                Roll = math.degrees(y - Roll0) +2
                Yaw = math.degrees(z - Yaw0) -150
                
                print("%f %f %f" % (Pitch,Roll,Yaw))
                
class ThreadControl (threading.Thread):
    def __init__(self, threadID, name,IMUData):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global Pitch
        global Roll
        global Yaw
        global z
        global M1
        global M2 
        global M3 
        global M4
        while True:
            M1 = 70 + 2.5*(0 - Pitch) - 2.5*(0 - Roll)
            M2 = 70 - 2.5*(0 - Pitch) + 2.5*(0 - Roll)
            M3 = 70 + 2.5*(0 - Pitch) - 2.5*(0 - Roll)
            M4 = 70 - 2.5*(0 - Pitch) + 2.5*(0 - Roll) 

class ThreadHTTP (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global Pitch
        global Roll
        global Yaw
        global M1
        global M2
        global M3
        global M4
        valx = 0
        valy = 0
        valz = 0
        while True:
            payload = {'Pitch': Pitch,'Roll': Roll,'Yaw': Yaw,'x': valx,'y': valy,'z': valz}
            try:
                r = requests.get("http://drone.ias-uniandes.com/setParameters_Quadcopter.php/get", params=payload,timeout=5,headers={'Connection': 'close'})
                rjson= r.json()
                jsonThrottle = float(rjson['Throttle'])
                jsonM1 = float(rjson['M1'])
                jsonM2 = float(rjson['M2'])
                jsonM3 = float(rjson['M3'])
                jsonM4 = float(rjson['M4'])
                r = requests.session()
                r.keep_alive = False
            except Exception,e:
                print "HTTP Get ERROR :("
            
            
# -------------------------------------------------- #




# -------------------------------------------------- #
# --- Main Thread ---------------------------------- #
# -------------------------------------------------- #

WelcomeMessage()
Init_Board()
[IMUSession,IMUData] = Init_IMU()

[Pitch0,Roll0,Yaw0] = GetInitialAngles(IMUData)

# Create new threads
thread1 = ThreadIMU(1, "IMU DAQ", IMUData)
thread2 = ThreadHTTP(2, "HTTP Control")
thread3 = ThreadControl(3, "Control Law")

# Start new Threads
thread1.start()
thread2.start()
# -------------------------------------------------- #