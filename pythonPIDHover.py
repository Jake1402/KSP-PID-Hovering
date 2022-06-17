import math
import krpc
import time
from PID import *


'''~~~setup~~~'''
conn = krpc.connect()
print(conn.krpc.get_status().version)

vessel = conn.space_center.active_vessel
vessel.control.sas = True
vessel.control.rcs = True
flightInfo = vessel.flight()

desiredAltitude = 45
timeToAlt = lambda h,a : math.sqrt((2*h)/a)
pid = PIDCon(1.75, 0.65, 2.0, 1.0, -1.0)
operation = True

'''~~~MAIN SCRIPT PART~~~'''
'''LAUNCH TO ALT'''
#F=ma
vessel.control.activate_next_stage()
acceleration = (vessel.max_thrust/vessel.mass)
burnTime = timeToAlt(desiredAltitude, acceleration)
vessel.control.throttle = 1
time.sleep(burnTime*0.0)
vessel.control.throttle = 0

'''Loop logic'''
dt=1/30
initTime = time.time_ns()
initTimeLoop = 0
prevError = 0
while operation:
    endTime = time.time_ns()
    time.sleep(1/30)
    '''PID CONTROL SYSTEM'''
    error = desiredAltitude - flightInfo.surface_altitude
    prop = pid.proportional(error)
    integral = pid.integral(error, dt)
    deriv = pid.derivative(dt, error, prevError)
    prevError = error
    summation = pid.sum(prop, integral, deriv)
    vessel.control.throttle = summation/50

    print("PROPORTIONAL - {} ~ INTEGRAL - {} ~ DERIVATIVE - {} ~ Sum - {} ~ Loop running for - {} ~ Throttle Position - {}".format(prop, integral, deriv, summation, ((time.time_ns()/(1000*1000*1000))-(initTime/(1000*1000*1000))), vessel.control.throttle))

    initTimeLoop = time.time_ns()

    dt = ((initTimeLoop-endTime)/(1000*1000*1000))



    #initTime = time.time_ns()
