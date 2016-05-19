import xml.etree.ElementTree
from track import Track
import track
e = xml.etree.ElementTree.parse("./sampleTracks.kml").getroot()

paths = []

PREFIX = "{http://www.opengis.net/kml/2.2}"



for path in e.iter(PREFIX + "coordinates"):
    curPath = []
    for point in path.text.strip().split(",0.0")[0:-1]:
        latLong = point.strip().split(",")
        curPath.append((latLong[1], latLong[0]),)
    paths.append(curPath)

tracks = []

for j, i in enumerate(paths):
    print("----------------{0}-----------------".format(j))
    t = Track(i)
    print(t.dist)
    print(t.maxIncline)
    print(t.meanIncline)
    tracks.append(t)

userPrefs = {"dist": 3.25, "facilities": True, "water": False, "incline": 2, "stairs": False}

res = track.closestTracks(tracks, userPrefs)

res = track.createJsonResponse(res)

print(res)
