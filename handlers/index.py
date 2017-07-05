#!/usr/bin/env python
#coding=utf-8

import tornado.escape
import tornado.web
from base import BaseHandler
import methods.db as db

class IndexHandler(BaseHandler):
  #@tornado.web.authenticated
  def get(self):
    #m_infos = db.select_blog_title(table='blogs',column='*')
    m_infos = self.db.query("select id,title from blogs")
    self.render("index.html",m_infos = m_infos,user=self.current_user)
