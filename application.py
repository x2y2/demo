#!/home/wangpei/venv/bin/python
#coding=utf8

import torndb
import redis
import tornado.web
from tornado.options import define,options
from url import url
from sessions.session import SessionManager
import os
import ConfigParser

class App(tornado.web.Application):
  def __init__(self):
    conf = ConfigParser.ConfigParser()
    conf.read('/home/wangpei/demo/config.py')
    self.mysql_host = conf.get('database','mysql_host')
    self.mysql_user = conf.get('database','mysql_user')
    self.mysql_password = conf.get('database','mysql_password')
    self.mysql_database = conf.get('database','mysql_database')
    self.mysql_charset = conf.get('database','mysql_charset')
    self.redis_host = conf.get('redis','redis_host')
    self.redis_port = conf.get('redis','redis_port')
    self.redis_password = conf.get('redis','redis_password')
    self.redis_db = conf.get('redis','redis_db')
    #define("mysql_host",default="127.0.0.1",help="database host")
    #define("mysql_user",default="wangpei",help="database user")
    #define("mysql_password",default="123456",help="database password")
    #define("mysql_database",default="suibi",help="database name")
    #define("mysql_charset",default="utf8mb4",help="database charset")

    #define("redis_host",default="127.0.0.1",help="reids host")
    #define("redis_port",default="6379",help="redis port")
    #define("redis_password",default="",help="redis password")
    #define("redis_db",default="0",help="redis db")

    settings = dict(template_path = os.path.join(os.path.dirname(__file__),"templates"),
                    static_path = os.path.join(os.path.dirname(__file__),"statics"),
                    cookie_secret = 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
                    session_secret = 'UlqOEysOTNOaRQS/+eiz3B3PhKNsnkQgsnl7L/LOSXc=',
                    session_timeout = 86400,
                    store_options = {
                    'redis_host': self.redis_host,
                    'redis_port': self.redis_port,
                    'redis_pass': self.redis_password,
                    },
                    xsrf_cookie = 'True',
                    debug = 'True',
                    login_url = '/login'
                    )
    super(App,self).__init__(url,**settings)
    self.db = torndb.Connection(
            host=self.mysql_host,
            database=self.mysql_database,
            user=self.mysql_user,
            password=self.mysql_password,
            charset=self.mysql_charset)
    if self.redis_password:
      self.redis = redis.StrictRedis(host=self.redis_host,
                                     port=self.redis_port,
                                     password=self.redis_password,
                                     db=self.redis_db)
    else:
      self.redis = redis.StrictRedis(host=self.redis_host,
                                     port=self.redis_port,
                                     db=self.redis_db)

    self.session_manager = SessionManager(settings["session_secret"],
                                          settings['store_options'])