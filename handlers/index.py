#!/usr/bin/env python
#coding=utf-8

import tornado.web
from base import BaseHandler


class IndexHandler(BaseHandler):
  #@tornado.web.authenticated
  def get(self):
    if self.current_user is not None:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
    else:
      login_user_pic = None;
      login_user_id = None;
    m_infos = self.db.query('''SELECT u.uid,u.pic,u.username,a.aid,a.title,a.content,a.created_at,a.comment_count,a.read_count 
                               FROM articles a,user u 
                               WHERE a.user_uid=u.uid 
                               ORDER BY created_at 
                               DESC''')
    count_article = self.db.query("SELECT count(aid) count FROM articles")
    self.render("index.html",m_infos=m_infos,login_user=self.current_user,login_user_pic=login_user_pic,login_user_id=login_user_id)
