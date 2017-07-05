import tornado.web

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