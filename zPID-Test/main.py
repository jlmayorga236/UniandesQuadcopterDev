# ----------------------------------------------------------- #
# -------- main.py for z-PID Drone con WebControl ----------- #
# ----------------------------------------------------------- #



# ----------------------------------------------------------- #
import requests
import random
import sys, getopt
import RTIMU
import os.path
import time
import math
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC


sys.path.append('.')
# ----------------------------------------------------------- #



# ----------------------------------------------------------- #
SETTINGS_FILE = "RTIMULib"
# ----------------------------------------------------------- #


# ----------------------------------------------------------- #
# ---- Define Function 
def computeHeight(pressure):
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));
# ----------------------------------------------------------- #


# ----------------------------------------------------------- #
# ---------- Init IMU --------------------------------------- #

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
    print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)

print("IMU Name: " + imu.IMUName())
print("Pressure Name: " + pressure.pressureName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded");

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

if (not pressure.pressureInit()):
    print("Pressure sensor Init Failed")
else:
    print("Pressure sensor Init Succeeded")

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

# --------------------------------------------------------------------------- #
ADC.setup()

PWM.start("P9_14", 50,500, 0)
PWM.set_duty_cycle("P9_14", 50.5)

time.sleep(poll_interval*5.0/1000.0)

PWM.set_duty_cycle("P9_14", 60.5)


valPitch = 0
valRoll = 0
valYaw = 0

valx = 0 
valy = 0 
valz = 0


while True:
    print "Busy \n"
    value = (ADC.read("P9_40")-0.5)*20 + 60
    PWM.set_duty_cycle("P9_14", value)
    print value

   
    if imu.IMURead():
        # x, y, z = imu.getFusionData()
        # print("%f %f %f" % (x,y,z))
        data = imu.getIMUData()
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
        fusionPose = data["fusionPose"] 

        valPitch = math.degrees(fusionPose[0])
        valRoll = math.degrees(fusionPose[1])
        valYaw = math.degrees(fusionPose[2])

        valx = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 
        valy = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 
        valz = computeHeight(data["pressure"])
        
        

        #payload = {'Pitch': valPitch,'Roll': valRoll,'Yaw': valYaw,'x': valx,'y': valy,'z': valz}
        #r = requests.get("http://drone.ias-uniandes.com/setParameters_Quadcopter.php/get", params=payload)
        #rjson = r.json()
        #jsonThrottle = float(rjson['Throttle'])

        #print jsonThrottle

        #time.sleep(poll_interval*1.0/1000.0)

print requests.get("http://drone.ias-uniandes.com/setParameters_Quadcopter.php/get", params=payload).json()