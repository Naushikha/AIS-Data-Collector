from math import atan2, sin, cos, sqrt


def defaultFilter(msg):
    # Get positional reports (class A) only
    if msg["msg_type"] in [1, 2, 3]:
        return True
    return False


def filter(msgDictList, filterFunc=defaultFilter):
    filteredMsgs = []
    for msg in msgDictList:
        if filterFunc(msg):
            filteredMsgs.append(msg)
    return filteredMsgs


def printTimeDifferenceList(msgDictList):
    prevTime = 0
    currTime = 0
    for msg in msgDictList:
        prevTime = currTime
        currTime = int(msg["epoch_time"])
        print(currTime - prevTime)


def printVesselList(msgDictList):
    vesselSet = set()
    for msg in msgDictList:
        vesselSet.add(msg["mmsi"])
    print(*sorted(vesselSet), sep="\n")


def printMapBounds(msgDictList):
    minLon = float(min(msgDictList, key=lambda x: x["lon"])["lon"])
    maxLon = float(max(msgDictList, key=lambda x: x["lon"])["lon"])
    minLat = float(min(msgDictList, key=lambda x: x["lat"])["lat"])
    maxLat = float(max(msgDictList, key=lambda x: x["lat"])["lat"])
    print(f"from ({minLat}, {minLon}) to ({maxLat}, {maxLon})")


# Based on Fossen's equations lat lon to flat
# https://github.com/cybergalactic/MSS/blob/master/GNC/llh2flat.m

originLat = 6.955879
originLon = 79.844690
a = 6378137  # semi-minor axis (equatorial radius)
e = 0.0818  # Earth eccentricity (WGS-84)
commonDenom = sqrt(1 - e**2 * sin(originLat) ** 2)
RN = a / commonDenom
RM = RN * (1 - e**2) / commonDenom


def computeFlatX(lon):
    deltaLon = lon - originLon
    return deltaLon / atan2(1, RN * cos(originLat))


def computeFlatY(lat):
    deltaLat = lat - originLat
    return deltaLat / atan2(1, RM)


# Approximate lat lon to X, Y
# https://sciencing.com/convert-distances-degrees-meters-7858322.html


def approximateFlatX(lon):
    deltaLon = lon - originLon
    return deltaLon * 111139  # Meters


def approximateFlatY(lat):
    deltaLat = lat - originLat
    return deltaLat * 111139  # Meters