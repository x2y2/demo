#!/usr/bin/env python
#encoding=utf8


import tornado.ioloop
import tornado.httpserver
import sys
from application import Application

reload(sys)
sys.setdefaultencoding('utf8')


def main():
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(8000)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()

