#!/usr/bin/env python
#encoding=utf8

import tornado.ioloop
import tornado.httpserver
import tornado.options
import sys
from application import App

reload(sys)
sys.setdefaultencoding('utf8')

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(App())
  http_server.listen(8000)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()

