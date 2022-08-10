import math

class InertialNavigation:

    toRadians = lambda self, theta : theta * (math.pi/180)
    toDegrees = lambda self, theta : theta * (180/math.pi)
    binaryStep = lambda self, x : (
        (2*(not x < 0))-1
    )
    sinSqr = lambda x : math.sin(x) * math.sin(x)

    def __init__(self):
        pass

    '''
    HAVERSINE FORMULA
    https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    '''
    def distanceBetweenCoordinates(self, coor1, coor2, bodyRadius):
        lat1 = coor1[0]
        long1 = coor1[1]
        lat2 = coor2[0]
        long2 = coor2[1]
        d=float(lat2-lat1)
        latDistanceRadians = self.toRadians(d)
        d=float(long2-long1)
        longDistanceRadians = self.toRadians(d)

        a = (
            self.sinSqr(float(latDistanceRadians/2)) +
            math.cos(self.toRadians(lat1)) * math.cos(self.toRadians(lat2)) *
            self.sinSqr(longDistanceRadians)
        )

        c = (
            2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        )

        distanceKM = bodyRadius * c

        return distanceKM*1000

    def getInformationFromAcceleration(self, acc, dt):
        info = [acc,0,0]
        info[1] = acc*dt
        info[2] = 0.5*acc*dt*dt

        return tuple(info)