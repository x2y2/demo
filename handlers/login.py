#!/usr/bin/env python
#coding=utf-8

import tornado.escape
import tornado.web
from base import BaseHandler
import base64
import re

    
class LoginHandler(BaseHandler):
  def get(self):
    self.render("login.html")

  def post(self):
    email = self.get_body_argument("email")
    password = self.get_body_argument("password")
    password = base64.b64encode(password)
    cbox_remember = self.get_body_argument("cbox_remember",default="off")

    if not self._checkemail_action(email):
      self.redirect("/sign_up?error=not_exists&user={0}".format(email))
    else:
      if not self._checkpasswd_action(email,password):
        self.redirect("/login?error=passwd_error")
      else:
        ret = self.db.query("SELECT username FROM user WHERE email=%s",email)
        username = ret[0]['username']
        if cbox_remember == "on":
          self.set_secure_cookie("username",username,expires_days=30)
        else:
          self.set_secure_cookie("username",username,expires_days=1)
        self.redirect('/')

  def _checkemail_action(self,email):
    id = self.db.query("SELECT id FROM user WHERE email=%s",email)
    if len(id) == 0:
      return False
    else:
      return True

  def _checkpasswd_action(self,email,password):
    id = self.db.query("SELECT id FROM user WHERE (email=%s and password=%s)",email,password)
    if not id:
      return False
    else:
      return True

  def _has_cn(self,text):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    return zhPattern.search(text)
      


  