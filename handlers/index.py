#!/usr/bin/env python
#coding=utf-8

import tornado.web
import methods.db as db

class IndexHandler(tornado.web.RequestHandler):
  def get(self):
    usernames = db.select_columns(table='user',column='username')
    one_user = usernames[0][0]
    self.render("index.html",user=one_user)

  def post(self):
    username = self.get_argument("username")
    password = self.get_argument("password")
    user_infos = db.select_table(table="user",column="*",condition="username",value=username)
    if user_infos:
      db_pwd = user_infos[0][2]
      if db_pwd == password:
        self.write(username)
      else:
        self.write("-1")
    else:
      self.write("-1")

  