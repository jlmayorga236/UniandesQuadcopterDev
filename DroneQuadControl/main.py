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
import csv
from pyBBBDrone import *
import Adafruit_BBIO.ADC as ADC
# -------------------------------------------------- #




# -------------------------------------------------- # 
# ---  Global Variables  --------------------------- #
# -------------------------------------------------- #
global Pitch
global Roll
global Yaw
global M1
global M2
global M3
global M4
global oPitch
global oRoll
global oYaw
global z
oPitch = 0.0
oRoll = 0
oYaw = 0
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
        global oPitch
        global oRoll
        global oYaw
	global z
        path = "ExpLQR.csv"
	with open(path, "wb") as csv_file:
        	writer = csv.writer(csv_file, delimiter=',')
		while True:
		    k = 0
		    while k<20:
		        k = k + 1
		        x, y, z = IMUData.getFusionData()
		        Pitchm = math.degrees(x - Pitch0) -3
		        Rollm = math.degrees(y - Roll0) +2
		        Yawm = math.degrees(z - Yaw0) -150
		        if IMUData.IMURead():
		            x, y, z = IMUData.getFusionData()
		            Pitchm = 1/25*Pitchm + math.degrees(x - Pitch0) -3
		            Rollm = 1/25*Rollm + math.degrees(y - Roll0) +2
		            Yawm = 1/25*Yawm + math.degrees(z - Yaw0) -150
		    oPitch=Pitchm/5
		    oRoll = Rollm/5
		    oYaw = Yawm/5
		    k = 0
		    while k<15:
		        k = k + 1
		        x, y, z = IMUData.getFusionData()
		        Pitchm = math.degrees(x - Pitch0) -3
		        Rollm = math.degrees(y - Roll0) +2
		        Yawm = math.degrees(z - Yaw0) -150
		        if IMUData.IMURead():
		            x, y, z = IMUData.getFusionData()
		            Pitchm = 1/25*Pitchm + math.degrees(x - Pitch0) -3
		            Rollm = 1/25*Rollm + math.degrees(y - Roll0) +2
		            Yawm = 1/25*Yawm + math.degrees(z - Yaw0) -150
		        Pitch=Pitchm/5
		        Roll = Rollm/5
		        Yaw = Yawm/5
		    
		    line1 = str(Pitch) + " , " +str(Roll) + " , "+str(Yaw) + " , " + str(z) 
		    line = line1.split(",")
		    writer.writerow(line)

                
class ThreadControl (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global Pitch
        global Roll
        global Yaw
        global oPitch
        global oRoll
        global oYaw
        global z
        global M1
        global M2 
        global M3 
        global M4
        while True:
		M1 = 0.5*max(-5,min(5,0  + 0.1*(0 - Roll) + 0.1*(0 - Pitch)  + 0.25*(Roll - oRoll) + 0.25*(Pitch - oPitch) ))
		M2 = 0.5*max(-5,min(5,0  - 0.1*(0 - Roll) + 0.1*(0 - Pitch)  + 0.25*(Roll - oRoll) + 0.25*(Pitch - oPitch)))
		M3 = 0.5*max(-5,min(5,0  + 0.1*(0 - Roll) - 0.05*(0 - Pitch)   + 0.25*(Roll - oRoll) + 0.25*(Pitch - oPitch)))
		M4 = 0.5*max(-5,min(5,0  - 0.1*(0 - Roll) - 0.05*(0 - Pitch)   + 0.25*(Roll - oRoll) + 0.25*(Pitch - oPitch)))
		z = -397*ADC.read("P9_40")+166
		TH = z
		print TH	
		TH = 90
		SetMotorsPWM(TH,M1,M2,M3,M4)
		print " "
		print("M1: %f M2: %f M3: %f M4: %f" % (M1,M2,M3,M4))
		print("Pitch: %f Roll: %f  Yaw : %f" % (Pitch,Roll,Yaw))
		print("z : %f cm " % (z))
		print " "
		time.sleep(0.35)

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
		print ""
                
             
            
            
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
thread3.start()
# -------------------------------------------------- #
