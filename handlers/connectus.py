#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler


class ContactusHandler(BaseHandler):
  def get(self):
    self.render("contactus.html",user=self.current_user,user_id=self.user_id)