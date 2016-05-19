import tornado.ioloop
import tornado.web
import os
from platform import system

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        print("main.html")
        self.finish()

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        print("test.html")
        self.finish()


settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static")
)


def make_app():
    print("make_app")
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", TestHandler),
    ], **settings)


if __name__ == "__main__":
    if system() in ("Windows", "Darwin"):
        port = 8888
    else:
        port = 80
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()