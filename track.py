
from geopy.distance import vincenty
import requests
import math
import json
import numpy as np

key = "AIzaSyDSm_uEB6ImW4x5Az6ghGocQ977id4LYzs"
url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={0},{1}|{2},{3}&key={4}'
multurl = 'https://maps.googleapis.com/maps/api/elevation/json?locations={0}&key={1}'


COOR = "{0},{1}"
LAT = 0
LONG = 1
INCLINE_EASY_OPT = 0
INCLINE_MEDIUM_OPT = 3
INCLINE_HARD_OPT = 6

def closestTracks(self,tracks, userPrefs):
    tracksInRange = []
    for track in tracks:
        if (track.dist <= userPrefs['dist']+500) and (track.dist >= userPrefs['dist']-500):
            tracksInRange.append(track)
    grades = []
    for track in tracksInRange:
        grade = 0
        if 0 <= userPrefs['incline'] < 3:
            grade = abs(track - INCLINE_EASY_OPT)
        if 3 <= userPrefs['incline'] < 6:
            grade = abs(track - INCLINE_MEDIUM_OPT)
        if 6 <= userPrefs['incline'] <= 12:
            grade = abs(track - INCLINE_HARD_OPT)
        if userPrefs['facilities']:
            if track.hasFacilities:
                grade -= 2
            else:
                grade += 2
        if userPrefs['water']:
            if track.hasWater:
                grade -= 2
            else:
                grade += 2
        if userPrefs['stairs']:
            if track.hasStairs:
                grade -= 2
            else:
                grade += 2
        grades.append(grade)
    closestTracks = []
    for i in range(3):
        minIndex = np.argmin(grades)
        del grades[minIndex]
        closestTracks.append(tracksInRange[minIndex])
        del tracksInRange[minIndex]
    return closestTracks


def createJsonResponse(self, tracks):
    data = {"results":[]}
    for track in tracks:
        data['results'].append({'incline': track.incline, 'dist': track.dist, 'facilities': track.Facilities,
                                'water': track.hasWater, 'stairs': track.hasStairs})
    json_data = json.dumps(data)
    return json_data


def get_elevations(listOfCoordinates):

    MAX_SIZE = 60
    elevations = []

    for i in range(len(listOfCoordinates)//(MAX_SIZE+1) + 1):
        elevations_query = ""
        elevations_query += COOR.format(listOfCoordinates[i*MAX_SIZE][LAT], listOfCoordinates[i*MAX_SIZE][LONG])

        for coordinates in range(i*MAX_SIZE + 1, min(i*MAX_SIZE + MAX_SIZE, len(listOfCoordinates))):
            elevations_query += "|" + COOR.format(listOfCoordinates[coordinates][LAT], listOfCoordinates[coordinates][LONG])

        res = requests.get(multurl.format(elevations_query, key)).json()

        for j in res["results"]:
            elevations.append(float(j["elevation"]))

    return elevations


class Track:
    dist = 0
    maxIncline = 0
    meanIncline = 0
    hasFacilities = False
    hasWater = False
    hasStairs = False

    def __init__(self, listOfCoordinates):
        elevations = get_elevations(listOfCoordinates)
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
