class PIDCon:

    Pgain = 0.0
    Igain = 0.0
    Dgain = 0.0

    Integral = 0
    maxI = 1.0
    lowI = -1.0

    '''GETTERS'''
    def getPgain(self):
        return self.Pgain

    def getIgain(self):
        return self.Igain

    def getDgain(self):
        return self.Dgain
    
    def getMaxI(self):
        return self.maxI

    def getLowI(self):
        return self.lowI

    '''SETTERS'''
    def setPgain(self, Pgain):
        self.Pgain = Pgain

    def setIgain(self, Igain):
        self.Igain = Igain
        
    def setDgain(self, Dgain):
        self.Dgain = Dgain

    def getMaxI(self, maxI):
        self.maxI = maxI

    def getLowI(self, lowI):
        self.lowI = lowI


    '''CONSTRUCTOR'''
    def __init__(self, PGain, IGain, DGain, MaxI, LowI):
        self.Pgain = PGain
        self.Igain = IGain
        self.Dgain = DGain
    
        self.maxI = MaxI
        self.lowI = LowI

        

    '''PID Functions'''
    def derivative(self, dt, error, prevError):
        return ((error - prevError)/dt)*self.Dgain
        
    def integral(self, error, dt):

        self.Integral = (self.Integral + error*dt)*self.Igain

        if(self.Integral >= self.maxI):
            self.Integral = 1.0
            return 1
        elif(self.Integral <= self.lowI):
            self.Integral = -1.0
            return -1.0
        else:
            return self.Integral

    def proportional(self, error):
        return error*self.Pgain

    def sum(self, prop, integral, derived):
        return prop + integral + derived