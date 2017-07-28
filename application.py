#!/usr/bin/env python
#coding=utf8

import torndb
import tornado.web
from tornado.options import define,options
from url import url
import os

define("mysql_host",default="127.0.0.1",help="database host")
define("mysql_user",default="wangpei",help="database user")
define("mysql_password",default="123456",help="database password")
define("mysql_database",default="suibi",help="database name")
define("mysql_charset",default="utf8mb4",help="database charset")

settings = dict(template_path = os.path.join(os.path.dirname(__file__),"templates"),
                static_path = os.path.join(os.path.dirname(__file__),"statics"),
                cookie_secret = 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
                xsrf_cookie = 'True',
                debug = 'True',
                login_url = '/login'
               )

class Application(tornado.web.Application):
  def __init__(self):
    tornado.web.Application.__init__(self,url,**settings)
    self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password,
            charset=options.mysql_charset)

