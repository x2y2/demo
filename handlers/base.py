import tornado.web

class BaseHandler(tornado.web.RequestHandler):
  def get_current_user(self):
    return self.get_secure_cookie("username")

  def json(self,status,info):
    self.write({
      "status": status,
      "info": info
      })