import tornado.web
import hashlib

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
  def user_id(self):
    user = self.current_user
    if user is not None:
      id = self.db.query("SELECT id FROM user WHERE username=%s",user)
      user_id = str(id[0]['id'])
      str_md5 = hashlib.md5(user_id).hexdigest()
      user_id = str_md5[0:16]
      return user_id