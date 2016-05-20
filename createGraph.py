import xml.etree.ElementTree
import sys
from track import Track
import track
import pickle


def results(tracks, query):
    res = track.closestTracks(tracks, query)

    res = track.createJsonResponse(res)
    # with open("./resPickle.pickle", 'wb') as f:
    #     pickle.dump(res, f)
    return res


def read_tracks():
    with open("./tracks.pickle", "rb") as f:
        curTracks = pickle.load(f)
    return curTracks

if __name__ == "__main__":
    tracks = []
    if sys.argv[1] == "write":
        e = xml.etree.ElementTree.parse("./sampleTracks.kml").getroot()
        paths = []
        attributes = []
        PREFIX = "{http://www.opengis.net/kml/2.2}"
        for path in e.iter(PREFIX + "Placemark"):
            w = f = s = False
            for name in path.iter(PREFIX + "name"):
                print(name.text)
                w = name.text.find("w") != -1
                f = name.text.find("f") != -1
                s = name.text.find("s") != -1
            for coors in path.iter(PREFIX + "coordinates"):
                curPath = []
                for point in coors.text.strip().split(",0.0")[0:-1]:
                    latLong = point.strip().split(",")
                    curPath.append((latLong[1], latLong[0]),)
                attributes.append({"w": w, "f": f, "s": s})
                paths.append(curPath)

        # for path in e.iter(PREFIX + "coordinates"):
        #     curPath = []
        #     for point in path.text.strip().split(",0.0")[0:-1]:
        #         latLong = point.strip().split(",")
        #         curPath.append((latLong[1], latLong[0]),)
        #     paths.append(curPath)

        for j, i in enumerate(paths):
            print("----------------{0}-----------------".format(j))
            t = Track(i)
            t.hasFacilities = attributes[j]["f"]
            t.hasStairs = attributes[j]["s"]
            t.hasWater = attributes[j]["w"]
            print(t.dist)
            print(t.maxIncline)
            print(t.meanIncline)
            print("w:{0},f:{1},s:{2}".format(attributes[j]["w"], attributes[j]["f"], attributes[j]["s"]))
            tracks.append(t)

        with open("./tracks.pickle", 'wb') as f:
            pickle.dump(tracks, f)

    elif sys.argv[1] == "read":
        with open("./tracks.pickle", "rb") as f:
            tracks = pickle.load(f)
    else:
        print("wrong args")
        exit(0)

    userPrefs = {"dist": 3, "facilities": True, "water": False, "incline": 1, "stairs": False, 'lat': 31.783029,
                 'long': 35.210880}

    res = results(tracks, userPrefs)
    with open("./resPickle.pickle", 'wb') as f:
        pickle.dump(res, f)
