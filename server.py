import json
import pickle
import tornado.ioloop
import tornado.web
import os
import createGraph
from platform import system

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("main.html")
        self.finish()

class GetTrack(tornado.web.RequestHandler):
    def get(self):
        print("test.html")
        self.finish()


class GetResults(tornado.web.RequestHandler):
    def post(self):
        print("results")
        body = bytes.decode(self.request.body)
        print(body)
        body = json.loads(body)
        curReq = {"dist": float(body["dist"]), "facilities": body["facilities"].lower() == "true",
                  "water": body["water"].lower() == "true", "incline": int(body["incline"]),
                  "stairs": body["stairs"].lower() == "true", 'lat': float(body["lat"]), 'long': float(body["long"])}
        tracks = createGraph.read_tracks()
        res = createGraph.results(tracks, curReq)
        self.finish(res)

class GetTestTracks(tornado.web.RequestHandler):
    def get(self):
        print("testTracks")
        with open("./resPickle.pickle", "rb") as f:
            res = pickle.load(f)
        print(res)
        self.finish(res)

settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static")
)


def make_app():
    print("make_app")
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/track", GetTrack),
        (r"/test", GetTestTracks),
        (r"/tracks", GetResults),
    ], **settings)


if __name__ == "__main__":
    if system() in ("Windows", "Darwin"):
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
