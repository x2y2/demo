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
    username = self.get_argument("username")
    password = self.get_argument("password")
    user_infos = db.select_table(table="user",column="*",condition="username",value=username)
    pwd = user_infos[0][2]
    if user_infos:
      if pwd == password:
        self.set_secure_cookie("username",username)
        self.write(username)
      else:
        self.finish('密码错误')
    else:
      self.finish('该用户不存在')
      

  