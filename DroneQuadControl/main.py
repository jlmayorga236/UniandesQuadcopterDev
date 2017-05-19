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

[Pitch0,Roll0,Yaw0] = GetInitialAngles(IMUData)

while True:
    if IMUData.IMURead():
            x, y, z = IMUData.getFusionData()
            Pitch = math.degrees(x - Pitch0) -3
            Roll = math.degrees(y - Roll0) -3
            Yaw = math.degrees(z - Yaw0) -3
            print("%f %f %f" % (math.degrees(Pitch),math.degrees(Roll),math.degrees(Yaw)))
 
            # -------------------------------------------------- #