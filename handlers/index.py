#!/usr/bin/env python
#coding=utf-8

import tornado.escape
import tornado.web
from base import BaseHandler
import methods.db as db

class IndexHandler(BaseHandler):
  #@tornado.web.authenticated
  def get(self):
    pic_name = None
    if self.current_user is not None:
      pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
      pic_name = pic[0]['pic']
    m_infos = self.db.query("select u.id,u.username,u.pic,b.id blog_id,b.title,b.content,b.created_at from blogs b,user u where b.user_id=u.id order by created_at desc")
    blog_count = self.db.query("SELECT count(id) count FROM blogs")
    user = self.current_user
    self.render("index.html",m_infos = m_infos,user=user,user_id=self.user_id,pic_name=pic_name)
