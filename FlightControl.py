import krpc
import time
import math

class flightControl:

    prefAltitude = 0
    pid = None
    flightInfo = None
    vessel = None
    makeZeroWhenNegative = lambda x : x(not x<0)
    timeToAlt = lambda h,a : math.sqrt((2*h)/a)
    summationForPID = lambda PIDCon, dt, error, prevError : PIDCon.proportional(error) + PIDCon.derivative(dt, error, prevError) + PIDCon.integral(error, dt)

    '''WAYPOINTS ARE LISTS OF TUPLES [(LONG, LAT, ALT)]'''
    wayPoint = []
    pidControllers = []

    def setGains(self, Pgain, Igain, Dgain):
        self.pid.setPgain(Pgain)
        self.pid.setIgain(Igain)
        self.pid.setDgain(Dgain)

    def __init__(self, pidController, conn):
        self.pid = pidController
        self.vessel = conn.space_center.active_vessel
        self.vessel.control.sas = True
        self.vessel.control.rcs = True
        self.flightInfo = self.vessel.flight()

    def resetPID(self):
        self.pid.resetPID()

    def beginLaunch(self):
        self.vessel.control.activate_next_stage()
        for i in range(5):
           # time.sleep(1)
            print("T minus - {}".format(5-i))

    def control(self, dt, error, prevError):
        prop = self.pid.proportional(error)
        integral = self.pid.integral(error, dt)
        deriv = self.pid.derivative(dt, error, prevError)
        return self.pid.sum(prop, integral, deriv)
