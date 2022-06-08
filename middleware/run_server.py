from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from middel_server import app
from tornado.ioloop import IOLoop

s = HTTPServer(WSGIContainer(app))
s.listen(4431) 
IOLoop.current().start()