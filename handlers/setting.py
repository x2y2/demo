#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler

class SettingHandler(BaseHandler):
  def get(self):
    self.render("setting.html",user=self.current_user,user_id=self.user_id)