
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
INCLINE_MEDIUM_OPT = 7.5
INCLINE_HARD_OPT = 10
LENGTH_FLEXIBILITY = 0.75

def closestTracks(tracks, userPrefs):
    tracksInRange = []
    print("tracks: " + str(len(tracks)))
    for track in tracks:
        if (track.dist <= userPrefs['dist']+LENGTH_FLEXIBILITY) and (track.dist >= userPrefs['dist']-LENGTH_FLEXIBILITY):
            tracksInRange.append(track)
    grades = []
    print("tracks in range: " + str(len(tracksInRange)))
    for track in tracksInRange:
        grade = 0
        if userPrefs['incline'] == 1:
            grade = abs(track.maxIncline - INCLINE_EASY_OPT)
        if userPrefs['incline'] == 2:
            grade = abs(track.maxIncline - INCLINE_MEDIUM_OPT)
        if userPrefs['incline'] == 3:
            grade = abs(track.maxIncline - INCLINE_HARD_OPT)
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
        minDistance = math.inf
        for point in track.points:
            cur_dist = abs(vincenty(point, (userPrefs['lat'],userPrefs['long'])).km)
            if (cur_dist < minDistance):
                minDistance = cur_dist
                track.closestPoint = point
        grade += math.sqrt(minDistance)
        grades.append(grade)
    nearestTracks = []
    for i in range(3):
        minIndex = np.argmin(grades)
        del grades[minIndex]
        nearestTracks.append(tracksInRange[minIndex])
        del tracksInRange[minIndex]
        curPoints = nearestTracks[i].points[0:-1]
        while curPoints[0] != nearestTracks[i].closestPoint:
            temp = curPoints[0]
            for j in range(1, len(curPoints)):
                curPoints[j-1] = curPoints[j]
            curPoints[len(curPoints)-1] = temp
        curPoints.append(curPoints[0])
        nearestTracks[i].points = curPoints
    return nearestTracks


def createJsonResponse(tracks):
    data = {"results": []}
    for track in tracks:
        inc = 0
        if track.maxIncline <= INCLINE_MEDIUM_OPT:
            inc = 1
        elif track.maxIncline <= INCLINE_HARD_OPT:
            inc = 2
        else:
            inc = 3
        data['results'].append({'incline': inc, 'dist': track.dist, 'facilities': track.hasFacilities,
                                'water': track.hasWater, 'stairs': track.hasStairs, 'points': track.points})
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
    closestPoint = (0, 0)
    dist = 0
    maxIncline = 0
    meanIncline = 0
    hasFacilities = False
    hasWater = False
    hasStairs = False
    points = []

    def __init__(self, listOfCoordinates):
        self.points = listOfCoordinates
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
