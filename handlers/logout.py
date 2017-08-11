import tornado.escape
import tornado.web
from base import BaseHandler

class LogoutHandler(BaseHandler):
  def get(self):
      #self.clear_cookie("username")
      self.session["username"] = None
      self.session.save()
      self.redirect("/")