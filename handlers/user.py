#!/usr/bin/env python
#coding=utf-8

import tornado.web
import methods.db as db

class UserHandler(tornado.web.RequestHandler):
  def get(self):
    username = self.get_argument("user")
    user_infos = db.select_table(table="user",column="*",condition="username",value=username)
    self.render("user.html",users = user_infos)