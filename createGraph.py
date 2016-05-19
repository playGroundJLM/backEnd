import xml.etree.ElementTree
import sys
from track import Track
import track
import pickle

if __name__ == "__main__":
    tracks = []
    if sys.argv[1] == "write":
        e = xml.etree.ElementTree.parse("./sampleTracks.kml").getroot()
        paths = []

        PREFIX = "{http://www.opengis.net/kml/2.2}"

        for path in e.iter(PREFIX + "coordinates"):
            curPath = []
            for point in path.text.strip().split(",0.0")[0:-1]:
                latLong = point.strip().split(",")
                curPath.append((latLong[1], latLong[0]),)
            paths.append(curPath)

        for j, i in enumerate(paths):
            print("----------------{0}-----------------".format(j))
            t = Track(i)
            print(t.dist)
            print(t.maxIncline)
            print(t.meanIncline)
            tracks.append(t)

        with open("./tracks.pickle", 'wb') as f:
            pickle.dump(tracks, f)

    elif sys.argv[1] == "read":
        with open("./tracks.pickle", "rb") as f:
            tracks = pickle.load(f)
    else:
        print("wrong args")
        exit(0)

    userPrefs = {"dist": 3.25, "facilities": True, "water": False, "incline": 3, "stairs": False, 'lat': 31.783029,
                 'long': 35.210880}

    res = track.closestTracks(tracks, userPrefs)

    res = track.createJsonResponse(res)
    print(res)
    with open("./resPickle.pickle", 'wb') as f:
        pickle.dump(res, f)
