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

class EditBlogHandler(BaseHandler):
  def get(self,*args,**kwargs):
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)(*args,**kwargs)
    else:
      m_infos = db.select_blog_title(table='blogs',column='*')
      self.render("index.html",m_infos = m_infos,user = self.current_user)

  def _info_action(self,*args,**kwargs):
    blog_id = self.get_argument('id',default="")
    blog_title = db.select_content_byid(table='blogs',column='title',condition='id',value=blog_id)
    blog_content = db.select_content_byid(table='blogs',column='content',condition='id',value=blog_id)
    self.render("editblog.html",user=self.current_user,blog_id=blog_id,blog_title=blog_title,blog_content=blog_content)
  
  
  def post(self,*args,**kwargs):
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)()
    else:
      self.json("fail","no action")

  def _update_blog_action(self):
    blog_id = self.get_argument("blog_id",default="")
    blog_title = self.get_argument("blog_title",default="").encode('utf8')
    blog_content = self.get_argument("blog_content",default="").encode('utf8')
    try:
      db.update_blog_content(id=blog_id,user_id=1,user_name=self.current_user,title=blog_title,content=blog_content)
      self.json("success",blog_title)
    except Exception as e:
      self.json("error",str(e))
