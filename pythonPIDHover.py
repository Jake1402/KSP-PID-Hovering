import math
import krpc
import time
from PID import *
from FlightControl import *
from InertialNavigation import *

'''~~~setup~~~'''
conn = krpc.connect()
print(conn.krpc.get_status().version)
vessel = conn.space_center.active_vessel
flightInfo = vessel.flight()

initAltitude = flightInfo.surface_altitude
initLatitude = flightInfo.latitude
initLongitude = flightInfo.longitude
desiredAltitude = 100

print("LATITUDE - {} ~ LONGTITUDE - {} ~ DESIRED ALT - {}".format(initLatitude, initLongitude, desiredAltitude))

pid = PIDCon(1.55, 1.1, 7.75, 35.0, -35.0)
#pidLong = PIDCon(5.0, 1.1, 8, -5.0, 5.0)
#pidLatitude = PIDCon(5.0, 1.1, 8, -5.0, 5.0)

controllerVertical = flightControl(pid, conn)
#controllerLong = flightControl(pidLong, conn)
#controllerLatitude = flightControl(pidLatitude, conn)

inertNav = InertialNavigation()

operation = True

'''~~~MAIN SCRIPT PART~~~'''
controllerVertical.beginLaunch()
dt=1/30
initTime = time.time_ns()
initTimeLoop = 0
prevError = 0
prevLongError = 0
prevLatError = 0

initFuel = vessel.mass - vessel.dry_mass
while operation:

    endTime = time.time_ns()
    time.sleep(1/30)

    '''PID CONTROL SYSTEM VERTICAL SYSTEM'''
    error = desiredAltitude - flightInfo.surface_altitude
    #print(error)
    summation = controllerVertical.control(dt, error, prevError)
    prevError = error
    #vessel.control.throttle = summation/50

    '''PID CONTROL SYSTEM HORIZONTAL SYSTEM'''
    '''
    a = (initLongitude - flightInfo.longitude)
    errorLong = (
        inertNav.distanceBetweenCoordinates((0, initLongitude), (0, flightInfo.longitude), 600)
        *inertNav.binaryStep(a)
    )
    a = (initLatitude - flightInfo.latitude)
    errorLatitude = (
        inertNav.distanceBetweenCoordinates((0, initLatitude), (0, flightInfo.latitude), 600)
        * inertNav.binaryStep(a)
    )
    summationLong = controllerLong.control(dt, errorLong, prevLongError)
    summationLatitude = controllerLatitude.control(dt, errorLatitude, prevLatError)
    
    prevLongError = errorLong
    prevLatError = errorLatitude

    vessel.control.up = -math.floor(summationLatitude)
    vessel.control.right = math.floor(summationLong)
        '''
    '''
    print("UP CONTROL - {} ~ RIGHT CONTROL - {} ~ OUT LAT - {} ~ OUT LONG - {}".format(
        vessel.control.up, vessel.control.right, summationLatitude, summationLong
    ))

    '''
    #print(errorLong)
    #print(flightInfo.longitude, initLongitude, flightInfo.latitude, initLatitude)
    #check if we should begin landing
    currentFuel = (vessel.mass - vessel.dry_mass)
    if((currentFuel/initFuel) <= 0.75):
        operation = False

    initTimeLoop = time.time_ns()
    dt = ((initTimeLoop-endTime)/(1000*1000*1000))


'''SWITCHING TO LANDING PHASE'''

print("landing!")
controllerVertical.resetPID()
vessel.control.brakes = True
landing = True
while landing:

    endTime = time.time_ns()
    time.sleep(1/30)

    '''PID CONTROL SYSTEM'''
    error = initAltitude - flightInfo.surface_altitude
    summation = controllerVertical.control(dt, error, prevError)
    prevError = error
    vessel.control.throttle = summation/50

    '''PID CONTROL SYSTEM HORIZONTAL SYSTEM'''
    '''
    a = (initLongitude - flightInfo.longitude)
    errorLong = (
        inertNav.distanceBetweenCoordinates((0, initLongitude), (0, flightInfo.longitude), 600)
        *inertNav.binaryStep((initLongitude - flightInfo.longitude))
    )
    a = (initLatitude - flightInfo.latitude)
    errorLatitude = (
        inertNav.distanceBetweenCoordinates((0, initLatitude), (0, flightInfo.latitude), 600)
        * inertNav.binaryStep(a)
    )
    summationLong = controllerLong.control(dt, errorLong, prevLongError)
    summationLatitude = controllerLatitude.control(dt, errorLatitude, prevLatError)

    prevLongError = errorLong
    prevLatError = errorLatitude

    vessel.control.up = -math.floor(summationLatitude)
    vessel.control.right = math.floor(summationLong)

    print("UP CONTROL - {} ~ RIGHT CONTROL - {} ~ OUT LAT - {} ~ OUT LONG - {}".format(
        vessel.control.up, vessel.control.right, summationLatitude, summationLong
    ))
'''
    #check if we should begin landing
    currentFuel = vessel.mass - vessel.dry_mass
    if(abs(error) <= 1 and (flightInfo.speed) < 1.5):
        landing = False

    initTimeLoop = time.time_ns()
    dt = ((initTimeLoop-endTime)/(1000*1000*1000))

vessel.control.throttle = 0