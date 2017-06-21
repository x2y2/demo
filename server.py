#!/usr/bin/env python
#encoding=utf8

import sys
import tornado.ioloop
import tornado.options
import tornado.httpserver

from application import application

from tornado.options import define,options
reload(sys)
sys.setdefaultencoding('utf8')
define("port",default = 8000,help = "run on the given port",type = int)

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(options.port)
  #http_server.bind(options.port)
  #http_server.start(4)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()

  
