# -------------------------------------------------- # 
# ---  Library : Board Library --------------------- #
# -------------------------------------------------- #


# -------------------------------------------------- # 
# ---  Import Modules ------------------------------ #
import requests
import random
import sys, getopt
import RTIMU
import time
import math
import threading
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import os.path
# -------------------------------------------------- #



# -------------------------------------------------- #
# --- Parameters  ---------------------------------- #
# -------------------------------------------------- #
global BoardVersion 
BoardVersion= 3.2
global SETTINGS_FILE
SETTINGS_FILE = "RTIMULib"
W1_0 = 50 # % PWM's Duty Cycle  
W2_0 = 50 # % PWM's Duty Cycle 
W3_0 = 50 # % PWM's Duty Cycle 
W4_0 = 50 # % PWM's Duty Cycle 
# -------------------------------------------------- #




# --------------------------------------------------- #
# --- def 1.1 WelcomeMessage() ---------------------- #
# --------------------------------------------------- #
def WelcomeMessage():
    print ".............................................."
    print " "
    print " "
    print "Bienvenido a una sesion con el Drone Quadcopter"
    print " "
    print " "
    print "     Board Version : " + str(BoardVersion)
    print "     IMU Settings File : "+ SETTINGS_FILE
# --------------------------------------------------- #


# --------------------------------------------------- #
# --- def 1.2 Init_Board() -------------------------- #
# --------------------------------------------------- #
def Init_Board():
    print "......................."
    print "Init_Board ..."
    print " "
    print "     Initing ADC module"
    ADC.setup()
    print "     ADC OK"
    print " "
    print "     Initing PWM Modules"
    PWM.start("P9_14", 50,500, 0)
    PWM.start("P9_16", 50,500, 0)
    PWM.start("P9_21", 50,500, 0)
    PWM.start("P9_22", 50,500, 0)
    print "     OWM OK"
    print " "    
    # Delay for Motors Set Up
    time.sleep(0.1)
    PWM.start("P9_14", 62,500, 0)
    PWM.start("P9_16", 62,500, 0)
    PWM.start("P9_21", 62,500, 0)
    print "Everthing OK in Init_Board XD No ban please :P"
    print " "
# --------------------------------------------------- #



# --------------------------------------------------- #
# --- def 1.2 Init_IMU()-- -------------------------- #
# --------------------------------------------------- #
def Init_IMU():
    print  "......................."
    print("Using settings file " + SETTINGS_FILE + ".ini")
    if not os.path.exists(SETTINGS_FILE + ".ini"):
        print("Settings file does not exist, will be created")
    print " "
    s = RTIMU.Settings(SETTINGS_FILE)
    imu = RTIMU.RTIMU(s)
    print " Setting IMU Preferences"
    print("IMU Name: " + imu.IMUName())
    print " "
    if (not imu.IMUInit()):
        print("IMU Init Failed")
        sys.exit(1)
    else:
        print("IMU Init Succeeded");
    # Fusion Parameters
    imu.setSlerpPower(0.02)
    imu.setGyroEnable(True)
    imu.setAccelEnable(True)
    imu.setCompassEnable(True)
    return (s,imu)
# --------------------------------------------------- #

# --------------------------------------------------- #
# --- def 1.3 SetMotorsPWM() ------------------------ #
# --------------------------------------------------- #
def SetMotorsPWM(Throttle,M1,M2,M3,M4):
    PWM.set_duty_cycle("P9_14", Throttle+M1)
    PWM.set_duty_cycle("P9_16", Throttle+M2)
    PWM.set_duty_cycle("P9_21", Throttle+M3)
    PWM.set_duty_cycle("P9_22", Throttle+M4)
# --------------------------------------------------- #

