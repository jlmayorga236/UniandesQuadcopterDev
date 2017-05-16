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


while True:
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



