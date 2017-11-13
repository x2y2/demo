#!/usr/bin/env python
#coding=utf-8

import tornado.web
from base import BaseHandler

class IndexHandler(BaseHandler):
  def get(self):
    self.login_user_infos()
    m_infos = self.db.query('''SELECT u.uid,u.pic,u.username,a.aid,a.title,a.content,a.created_at,a.comment_count,a.read_count 
                               FROM articles a,user u 
                               WHERE a.user_uid=u.uid 
                               ORDER BY created_at 
                               DESC''')
    count_article = self.db.query("SELECT count(aid) count FROM articles")
    self.render("index.html",m_infos=m_infos,user_infos=self.user_infos)
