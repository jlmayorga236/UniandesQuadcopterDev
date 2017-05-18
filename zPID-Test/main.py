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

#print("Using settings file " + SETTINGS_FILE + ".ini")
#if not os.path.exists(SETTINGS_FILE + ".ini"):
    #print("Settings file does not exist, will be created")

#s = RTIMU.Settings(SETTINGS_FILE)
#imu = RTIMU.RTIMU(s)
#pressure = RTIMU.RTPressure(s)

#print("IMU Name: " + imu.IMUName())
#print("Pressure Name: " + pressure.pressureName())

#if (not imu.IMUInit()):
    #print("IMU Init Failed")
    #sys.exit(1)
#else:
    #print("IMU Init Succeeded");

# this is a good time to set any fusion parameters

#imu.setSlerpPower(0.02)
#imu.setGyroEnable(True)
#imu.setAccelEnable(True)
#imu.setCompassEnable(True)

#if (not pressure.pressureInit()):
    #print("Pressure sensor Init Failed")
#else:
    #print("Pressure sensor Init Succeeded")
poll_interval = 1
#poll_interval = imu.IMUGetPollInterval()
#print("Recommended Poll Interval: %dmS\n" % poll_interval)

# --------------------------------------------------------------------------- #
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
time.sleep(poll_interval*1.0/1000.0)
print "Thats it, ready to go"
PWM.set_duty_cycle("P9_14", 60.5)
PWM.set_duty_cycle("P9_16", 60.5)
PWM.set_duty_cycle("P9_21", 60.5)
PWM.set_duty_cycle("P9_22", 60.5)
                   

valPitch = 0
valRoll = 0
valYaw = 0

valx = 0 
valy = 0 
valz = 0

k = 0

jsonThrottle = 50
jsonM1 = jsonThrottle + 3
jsonM2 = jsonThrottle + 2
jsonM3 = jsonThrottle
jsonM4 = jsonThrottle - 2

print "Entering while loop"

while True:
    k = k +1
    print "-----------------------------------------------"
    print "Starting Iteration ["+str(k)+"]"
    print "-----------------------------------------------"
    print " "
    print " "
    print "Reading ADC Value ...."
    zValue= 100-100*ADC.read("P9_40")
    print "Requesting GET ..."
    payload = {'Pitch': valPitch,'Roll': valRoll,'Yaw': valYaw,'x': valx,'y': valy,'z': valz}
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
    
    PWM.set_duty_cycle("P9_14", jsonM1)
    PWM.set_duty_cycle("P9_16", jsonM2)
    PWM.set_duty_cycle("P9_21", jsonM3)
    PWM.set_duty_cycle("P9_22", jsonM4)
    
    print "W0:[" + str(jsonThrottle) + "]%"
    print "---------------------------------"

    
   
