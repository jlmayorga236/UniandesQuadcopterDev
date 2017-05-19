# -------------------------------------------------- # 
# ---  Library : Board Library --------------------- #
# -------------------------------------------------- #


# -------------------------------------------------- # 
# ---  Import Modules  ----------------------------- #
# -------------------------------------------------- #
import random
import time
import math
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
# --- Main Thread ---------------------------------- #
# -------------------------------------------------- #

WelcomeMessage()
Init_Board()
[IMUSession,IMUData] = Init_IMU()

while True:
    if IMUData.IMURead():
            x, y, z = IMUData.getFusionData()
            print("%f %f %f" % (x,y,z))
            data = imu.getIMUData()
            (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = pressure.pressureRead()
            fusionPose = data["fusionPose"]
            print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))

            # -------------------------------------------------- #