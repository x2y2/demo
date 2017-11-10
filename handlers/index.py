#!/usr/bin/env python
#coding=utf-8

import tornado.web
from base import BaseHandler
from user_main import UserBaseHandler as UBH

class IndexHandler(UBH):
  def get(self):
    UBH.login_user_infos(self)
    m_infos = self.db.query('''SELECT u.uid,u.pic,u.username,a.aid,a.title,a.content,a.created_at,a.comment_count,a.read_count 
                               FROM articles a,user u 
                               WHERE a.user_uid=u.uid 
                               ORDER BY created_at 
                               DESC''')
    count_article = self.db.query("SELECT count(aid) count FROM articles")
    self.render("index.html",m_infos=m_infos,user_infos=UBH.user_infos)
