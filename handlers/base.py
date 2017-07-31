import tornado.web
import hashlib
import urlparse

class BaseHandler(tornado.web.RequestHandler):
  @property
  def db(self):
    return self.application.db

  def get_current_user(self):
    return self.get_secure_cookie("username")

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