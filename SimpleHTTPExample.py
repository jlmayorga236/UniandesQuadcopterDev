import requests
import random
''' Test commment'''
valPitch = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 
valRoll = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 
valYaw = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 

valx = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 
valy = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 
valz = float( random.randrange(1, 100, 1))/float(random.randrange(1,50, 1)) 


payload = {'Pitch': valPitch,'Roll': valRoll,'Yaw': valYaw,'x': valx,'y': valy,'z': valz}
r = requests.get("http://drone.ias-uniandes.com/setParameters_Quadcopter.php/get", params=payload)
rjson = r.json()
jsonThrottle = float(rjson['Throttle'])
print jsonThrottle
