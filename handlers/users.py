#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
import hashlib


class UsersHandler(BaseHandler):
  def get(self):
    pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
    pic_name = pic[0]['pic']
    self.render("users.html",user=self.current_user,user_id=self.user_id,pic_name=pic_name)

class UserArticleHandler(BaseHandler):  
  def get(self):
    query = self.get_argument("order_by",default="")
    action = "_%s" % query
    count_article = self.db.query('''SELECT 
                                        COUNT(*) count
                                     FROM 
                                        blogs 
                                     WHERE 
                                        user_name=%s
                                  ''',
                                  self.current_user
                                  )
    if hasattr(self,action):
      getattr(self,action)(count_article)

  def _created_at(self,count_article):
    read = 0
    comment = 0
    good = 0
    pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
    pic_name = pic[0]['pic']
    m_infos = self.db.query('''SELECT 
                                  u.pic,
                                  b.id,
                                  b.user_name,
                                  b.title,
                                  b.content,
                                  b.created_at 
                               FROM 
                                  blogs b,
                                  user u 
                               WHERE 
                                  b.user_id=u.id 
                               AND 
                                  b.user_name=%s
                            ''',
                            self.current_user
                            )
    self.render("users.html",user=self.current_user,user_id=self.user_id,m_infos=m_infos,count_article=count_article,read=read,
                 comment=comment,good=good,pic_name=pic_name)

  def _commented_at(self,count_article):
    pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
    pic_name = pic[0]['pic']
    self.render("commented.html",user=self.current_user,pic_name=pic_name,user_id=self.user_id,count_article=count_article)


    

