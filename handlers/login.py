#!/usr/bin/env python
#coding=utf-8

import tornado.escape
import tornado.web
import methods.db as db
from base import BaseHandler

    
class LoginHandler(BaseHandler):
  def get(self):
    self.render("login.html")

  def post(self):
    username = self.get_body_argument("username")
    password = self.get_body_argument("password")
    cbox_remember = self.get_body_argument("cbox_remember",default="off")

    if not self._checkusername_action(username):
      self.redirect("/login?error=not_exists&user={0}".format(username))
    else:
      if not self._checkpasswd_action(username,password):
        self.redirect("/login?error=passwd_error")
      else:
        if cbox_remember == "on":
          self.set_secure_cookie("username",username,expires_days=30)
        else:
          self.set_secure_cookie("username",username,expires_days=1)
        self.redirect('/')

  def _checkusername_action(self,username):
    #user_infos = user_infos = db.select_table(table="user",column="*",condition="username",value=username)
    #user = user_infos[0][1]
    user = self.db.query("select id from user where username='{0}'".format(username))
    if len(user) == 0:
      return False
    else:
      return True

  def _checkpasswd_action(self,username,password):
    #user_infos = user_infos = db.select_table(table="user",column="*",condition="username",value=username)
    #user = user_infos[0][0]
    user = self.db.query("select id from user where (username='{0}' and password={1})".format(username,password))
    if not user:
      return False
    else:
      return True
      


  