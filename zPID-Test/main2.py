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
import threading


sys.path.append('.')
# ----------------------------------------------------------- #



# ----------------------------------------------------------- #
SETTINGS_FILE = "RTIMULib"
# ----------------------------------------------------------- #


# ----------------------------------------------------------- #
# ---- Define Function 
def computeHeight(pressure):
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));
def init_Board():
    print "HI! Welcome to Dron Uniandes Dev & Resch"
    print  "......."
    print  "Initing ADC Pot..."
    ADC.setup()
    print  "Initing PWM Ports for P19_14...P19_22"
    PWM.start("P9_14", 50,500, 0)
    PWM.start("P9_16", 50,500, 0)
    PWM.start("P9_21", 50,500, 0)
    PWM.start("P9_22", 50,500, 0)

    PWM.set_duty_cycle("P9_14", 50.5)
    PWM.set_duty_cycle("P9_16", 50.5)
    PWM.set_duty_cycle("P9_21", 50.5)
    PWM.set_duty_cycle("P9_22", 50.5)

    print "Waiting one second ...."
    time.sleep(0.5)
    print "Thats it, ready to go"
    PWM.set_duty_cycle("P9_14", 60.5)
    PWM.set_duty_cycle("P9_16", 60.5)
    PWM.set_duty_cycle("P9_21", 60.5)
    PWM.set_duty_cycle("P9_22", 60.5)
# ----------------------------------------------------------- #


# ----------------------------------------------------------- #
# ---------- Init IMU --------------------------------------- #
def init_IMU(SETTINGS_FILE):
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
        poll_interval = 1
        poll_interval = imu.IMUGetPollInterval()
        print("Recommended Poll Interval: %dmS\n" % poll_interval)
    return (imu,poll_interval)



init_Board()
[imu,poll_interval] = init_IMU(SETTINGS_FILE)    



# --------------------------------------------------------------------------- #

                   

valPitch = 0
valRoll = 0
valYaw = 0

valx = 0 
valy = 0 
valz = 0

Pitch = 0
Roll = 0
Yaw = 0

Pitch0 = 0
Roll0 = 0
Yaw0 = 0

k = 0

jsonThrottle = 50
jsonM1 = jsonThrottle + 3
jsonM2 = jsonThrottle + 2
jsonM3 = jsonThrottle
jsonM4 = jsonThrottle - 2

print "Entering while loop"

for x in range(0, 10):
    if imu.IMURead():
        # x, y, z = imu.getFusionData()
        # print("%f %f %f" % (x,y,z))
        data = imu.getIMUData()
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
        fusionPose = data["fusionPose"]
        print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), 
            math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
        if (data["pressureValid"]):
            print("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["pressure"])))
        if (data["temperatureValid"]):
            print("Temperature: %f" % (data["temperature"]))
        time.sleep(poll_interval*1.0/1000.0)

        Pitch = math.degrees(fusionPose[1]) - Pitch0
        Roll = math.degrees(fusionPose[2]) - Roll0
        Yaw = math.degrees(fusionPose[0]) - Yaw0

        Pitch0 = Pitch
        Roll0 = Roll
        Yaw0 = Yaw

while True:
    k = k +1
    print "-----------------------------------------------"
    print "Starting Iteration ["+str(k)+"]"
    print "-----------------------------------------------"
    print " "
    print " "
    #print "Reading ADC Value ...."
    zValue= 100-100*ADC.read("P9_40")
    #print "Requesting GET ..."
    payload = {'Pitch': Pitch,'Roll': Roll,'Yaw': Yaw,'x': valx,'y': valy,'z': zValue}
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
        print "Hola :( Tuvimos un error y lo ignoramos,espero que no pase otra vez XD"
	print e
    	print e
    if imu.IMURead():
        x, y, z = imu.getFusionData()
        data = imu.getIMUData()
        (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
        fusionPose = data["fusionPose"]
        #print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]), 
            #math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
        #if (data["pressureValid"]):
            #print("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["pressure"])))
        #if (data["temperatureValid"]):
            #print("Temperature: %f" % (data["temperature"]))
        time.sleep(poll_interval*1.0/1000.0)
        
        Pitch = math.degrees(fusionPose[1]) 
        Roll = math.degrees(fusionPose[2])
        Yaw = math.degrees(fusionPose[0]) 
        
        print Pitch
        print Roll
        print Yaw
        
        u1 = min(100,jsonM1 + 0.0*Pitch)
        u2 = min(100,jsonM2 + 0.0*Pitch)
        u3 = min(100,jsonM3 + 0.0*Roll)
        u4 = min(100,jsonM4 + 0.0*Roll)

    PWM.set_duty_cycle("P9_14", u1)
    PWM.set_duty_cycle("P9_16", u2)
    PWM.set_duty_cycle("P9_21", u3)
    PWM.set_duty_cycle("P9_22", u4)
    
    print "Pitch:[" + str(Pitch) + "] "+" Roll:[" + str(Roll) + "] " + " Yaw:[" + str(Yaw) + "] "
    print "M1 : " + str(u1) +  "M2 : " + str(u2)+  "M3 : " + str(u3)+  "M4 : " + str(u4)
    print "---------------------------------"

    
   
