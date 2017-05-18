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


valPitch = 0
valRoll = 0
valYaw = 0

valx = 0 
valy = 0 
valz = 0

k = 0
while True:
    print "Starting Iteration ["+str(k)+"]"
    print "Reading ADC Value ...."
    zValue= 45.325976
    print "Requesting GET ..."
    payload = {'Pitch': valPitch,'Roll': valRoll,'Yaw': valYaw,'x': valx,'y': valy,'z': valz}
    r = requests.get("http://drone.ias-uniandes.com/setParameters_Quadcopter.php/get", params=payload)
    print r.status_code
    bad_r.raise_for_status()
    rjson = r.json()
    jsonThrottle = float(rjson['Throttle'])
    jsonM1 = float(rjson['M1'])
    jsonM2 = float(rjson['M2'])
    jsonM3 = float(rjson['M3'])
    jsonM4 = float(rjson['M4'])
    
    print jsonThrottle

   