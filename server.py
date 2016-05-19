import pickle
import tornado.ioloop
import tornado.web
import os
from platform import system

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("main.html")
        self.finish()

class GetTrack(tornado.web.RequestHandler):
    def get(self):
        print("test.html")
        self.finish()

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
    ], **settings)


if __name__ == "__main__":
    if system() in ("Windows", "Darwin"):
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()