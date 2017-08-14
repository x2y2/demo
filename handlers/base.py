#coding=utf8

import tornado.web
import urlparse
from sessions.session import Session

class BaseHandler(tornado.web.RequestHandler):
  def __init__(self,*args,**kwargs):
    super(BaseHandler,self).__init__(*args,**kwargs)
    self.session = Session(self.application.session_manager,self)

  @property
  def db(self):
    return self.application.db

  @property
  def redis(self):
    return self.application.redis

  def get_current_user(self):
    #return self.get_secure_cookie("username")
    return self.session.get("username")

  def json(self,status,info):
    self.write({
      "status": status,
      "info": info
      })

  @property
  def id(self):
    url = self.request.uri
    ret = urlparse.urlparse(url)
    path = ret.path
    id = path.split('/')[2]
    return id

  @property
  def arg(self):
    url = self.request.uri
    ret = urlparse.urlparse(url)
    path = ret.path
    arg = path.split('/')[-1]
    return arg