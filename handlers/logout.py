import tornado.escape
import tornado.web
import methods.db as db
from base import BaseHandler

class LogoutHandler(BaseHandler):
  def get(self):
    if not self.get_argument("logout",None):
      self.clear_cookie("username")
      self.redirect("/login")