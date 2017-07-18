#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
import hashlib



class UsersHandler(BaseHandler):
  def get(self):
    uid = self.id
    if uid is None: 
      author_name = self.current_user
      count_article = self.db.query('''SELECT COUNT(*) count FROM blogs WHERE  user_name=%s''',self.current_user)[0]['count']
    else:
      author_name = self.db.query("select username from user where uid=%s",uid)[0]['username']
      count_article = self.db.query("SELECT COUNT(*) count FROM blogs WHERE  user_uid=%s",uid)[0]['count']
    #登录用户信息
    if self.current_user is not None:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
    else:
      login_user_pic = None
      login_user_id = None
    #作者信息
    if uid is None:
      author_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
    else:
      author_info = self.db.query("SELECT pic FROM user WHERE uid=%s",uid)
    author_pic = author_info[0]['pic']
    author_id = uid
    login_user = self.current_user
    #获取URL参数
    string = self.get_argument("order_by",default="")
    action = "_%s" % string
    if hasattr(self,action):
      getattr(self,action)(count_article,uid,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user)
    else:
      self.user_info(count_article,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user)

  #用户动态信息
  def user_info(self,count_article,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user):  
    self.render("user_info.html",
                 author_name=author_name,
                 login_user=self.current_user,
                 login_user_pic=login_user_pic,
                 login_user_id=login_user_id,
                 author_pic = author_pic,
                 author_id = author_id,
                 count_article=count_article)
  #文章
  def _created_at(self,count_article,uid,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user):
    m_infos = self.db.query('''SELECT
                                  u.uid u_id, 
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
                                  b.user_uid=u.uid 
                               AND 
                                  b.user_uid=%s
                               ORDER BY
                                  created_at
                               DESC
                            ''',
                            uid
                            )

    self.render("users.html",
                 author_name=author_name,
                 author_pic=author_pic,
                 author_id=author_id,
                 m_infos=m_infos,
                 uid=uid,
                 count_article=count_article,
                 login_user_pic=login_user_pic,
                 login_user_id=login_user_id,
                 login_user=login_user)
  #评论
  def _commented_at(self,count_article,uid,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user):
    self.render("commented.html",
                 author_name=author_name,
                 author_pic=author_pic,
                 author_id=author_id,
                 count_article=count_article,
                 login_user_pic=login_user_pic,
                 login_user_id=login_user_id,
                 login_user=login_user)


    

