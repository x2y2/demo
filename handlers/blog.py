#!/usr/bin/env python
#coding=utf8

import tornado.web
from base import BaseHandler
import methods.db as db
import sys
import datetime


reload(sys)
sys.setdefaultencoding('utf8')

class BlogContentHandler(BaseHandler):
  def get(self):
    uri = self.request.uri
    page = int(uri.split('/')[-1])
    b_infos = db.select_blog_content(table='blogs',column='*')
    b_infos = b_infos
    self.render("blog.html",b_infos=b_infos,user=self.current_user,page=page)

class NewBlogHandler(BaseHandler):
  def get(self,*args,**kwargs):
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)()
    else:
      m_infos = db.select_blog_title(table='blogs',column='*')
      self.render("index.html",m_infos = m_infos,user = self.current_user)

  def _info_action(self):
    self.render("newblog.html",user=self.current_user)

  def post(self,*args,**kwargs):
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)()
    else:
      self.json("fail","no aciton!")

  def _add_blog_action(self):
    blog_title = self.get_body_argument("blog_title",default="")
    blog_content = self.get_body_argument("blog_content",default="")
    id = db.select_blog_content(table="blogs",column="*")[-1][0]
    id = int(id) + 1
    created_at = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
    try:
      db.add_blog_content(id=id,user_id=1,user_name='wangpei',title=blog_title,content=blog_content,created_at=created_at)
      self.json("success",blog_title)
    except Exception as e:
      self.json("error",str(e))



    