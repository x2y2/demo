#!/usr/bin/env python
#coding=utf-8

import tornado.escape
import tornado.web
from base import BaseHandler
import methods.db as db

class IndexHandler(BaseHandler):
  #@tornado.web.authenticated
  def get(self):
    m_infos = self.db.query("select id,user_name,title,content,created_at from blogs order by created_at desc")
    blog_count = self.db.query("SELECT count(id) count FROM blogs")
    blog_summary = m_infos[0]['content']
    self.render("index.html",m_infos = m_infos,user=self.current_user,blog_count=blog_count)
