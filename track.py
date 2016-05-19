
from geopy.distance import vincenty
import requests
import math
key = "AIzaSyDSm_uEB6ImW4x5Az6ghGocQ977id4LYzs"
url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={0},{1}|{2},{3}&key={4}'
multurl = 'https://maps.googleapis.com/maps/api/elevation/json?locations={0}&key={1}'

COOR = "{0},{1}"
LAT = 0
LONG = 1

class Track:
    dist = 0
    maxIncline = 0
    meanIncline = 0
    hasFacilities = False
    hasWater = False
    hasStairs = False

    def __init__(self, listOfCoordinates):
        elevations_query = ""
        elevations_query += COOR.format(listOfCoordinates[0][LAT], listOfCoordinates[0][LONG])

        for coordinates in range(1, len(listOfCoordinates)):
            elevations_query += "|" + COOR.format(listOfCoordinates[coordinates][LAT], listOfCoordinates[coordinates][LONG])

        res = requests.get(multurl.format(elevations_query, key)).json()
        elevations = []
        for i in res["results"]:
            elevations.append(float(i["elevation"]))

        for location in range(1, len(listOfCoordinates)):
            cur_dist = abs(vincenty(listOfCoordinates[location-1], listOfCoordinates[location]).km)
            self.dist += cur_dist
            height1 = elevations[location]
            height2 = elevations[location-1]
            cur_inc = abs(math.degrees(math.atan(abs(height2 - height1) / (cur_dist * 1000))))
            if cur_inc >= self.maxIncline:
                self.maxIncline = cur_inc
            self.meanIncline += cur_inc * cur_dist * 1000
        self.meanIncline /= self.dist * 1000