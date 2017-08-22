#!/home/wangpei/venv/bin/python
#coding=utf8

import torndb
import redis
import tornado.web
from tornado.options import define,options
from url import url
from sessions.session import SessionManager
import os

class App(tornado.web.Application):
  def __init__(self):
    define("mysql_host",default="127.0.0.1",help="database host")
    define("mysql_user",default="wangpei",help="database user")
    define("mysql_password",default="123456",help="database password")
    define("mysql_database",default="suibi",help="database name")
    define("mysql_charset",default="utf8mb4",help="database charset")

    define("redis_host",default="127.0.0.1",help="reids host")
    define("redis_port",default="6379",help="redis port")
    define("redis_password",default="",help="redis password")
    define("redis_db",default="0",help="redis db")

    settings = dict(template_path = os.path.join(os.path.dirname(__file__),"templates"),
                    static_path = os.path.join(os.path.dirname(__file__),"statics"),
                    cookie_secret = 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
                    session_secret = 'UlqOEysOTNOaRQS/+eiz3B3PhKNsnkQgsnl7L/LOSXc=',
                    session_timeout = 86400,
                    store_options = {
                    'redis_host': options.redis_host,
                    'redis_port': options.redis_port,
                    'redis_pass': options.redis_password,
                    },
                    xsrf_cookie = 'True',
                    debug = 'True',
                    login_url = '/login'
                    )
    super(App,self).__init__(url,**settings)
    self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password,
            charset=options.mysql_charset)
    if options.redis_password:
      self.redis = redis.StrictRedis(host=options.redis_host,
                                     port=options.redis_port,
                                     password=options.redis_password,
                                     db=options.redis_db)
    else:
      self.redis = redis.StrictRedis(host=options.redis_host,
                                     port=options.redis_port,
                                     db=options.redis_db)

    self.session_manager = SessionManager(settings["session_secret"],
                                          settings['store_options'])