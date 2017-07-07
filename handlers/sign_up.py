#!/usr/bin/env python
#coding=utf-8

import tornado.escape
import tornado.web
import methods.db as db
from base import BaseHandler
import datetime
import base64

    
class SignUpHandler(BaseHandler):
  def get(self):
    self.render("sign_up.html")

  def post(self):
    username = self.get_body_argument("username",default="")
    email = self.get_body_argument("email",default="")
    password =  self.get_body_argument("password",default="")
    password = base64.b64encode(password)
    register_time = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
    if not self._checkusername_action(username,email):
      self.db.execute('''INSERT INTO user 
                        (
                         username,
                         email,
                         register_time,
                         password,
                         admin
                         )
                         VALUES
                         (
                          %s,
                          %s,
                          %s,
                          %s,
                          '0'
                         )''',
                         username,
                         email,
                         register_time,
                         password)
      self.redirect("/login")
    else:
      self.redirect("/sign_up?error=exists&user={0}&email=(1)".format(username,email))

  def _checkusername_action(self,username,email):
    user_id = self.db.query("SELECT id FROM user WHERE (username=%s or email=%s)",username,email)
    if len(user_id) == 0:
      return False
    else:
      return True