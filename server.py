#!/usr/bin/env python
#encoding=utf8

import sys
import torndb
import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.web

from application import settings
from url import url
from tornado.options import define,options
reload(sys)
sys.setdefaultencoding('utf8')

define("port",default = 8000,help = "run on the given port",type = int)
define("mysql_host",default="127.0.0.1",help="database host")
define("mysql_user",default="wangpei",help="database user")
define("mysql_password",default="123456",help="database password")
define("mysql_database",default="suibi",help="database name")
define("mysql_charset",default="utf8mb4",help="database charset")

class Application(tornado.web.Application):
  def __init__(self):
    tornado.web.Application.__init__(self,url,**settings)
    self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password,
            charset=options.mysql_charset)

def main():
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()

