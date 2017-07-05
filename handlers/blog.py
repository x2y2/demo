#!/usr/bin/env python
#coding=utf8

import tornado.web
from base import BaseHandler
import methods.db as db
import sys
import datetime
import hashlib


reload(sys)
sys.setdefaultencoding('utf8')

class BlogContentHandler(BaseHandler):
  def get(self):
    uri = self.request.uri
    page = uri.split('/')[-1]
    #b_infos = db.select_blog_content(table='blogs',column='*')
    b_infos = self.db.query("SELECT content FROM blogs WHERE id='{0}'".format(page))
    self.render("blog.html",b_infos=b_infos,user=self.current_user)

class NewBlogHandler(BaseHandler):
  def get(self,*args,**kwargs):
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)()
    else:
      m_infos = self.db.query("select id,title from blogs")
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
    user_name = self.current_user
    created_at = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
    str = ''.join([created_at,user_name])
    str_md5 = hashlib.md5(str).hexdigest()
    blog_id = str_md5[0:16]
    try:
      self.db.execute('''INSERT INTO blogs
                          (id,
                           user_id,
                           user_name,
                           title,
                           content,
                           created_at
                           )
                           VALUES
                           (%s,
                           (SELECT id FROM user WHERE username=%s),
                           %s,%s,%s,%s
                           )''',
                           blog_id,
                           user_name,
                           user_name,
                           blog_title,
                           blog_content,
                           created_at)
      self.json("success",blog_title)
    except Exception as e:
      self.json('error',str(e))

class EditBlogHandler(BaseHandler):
  def get(self,*args,**kwargs):
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)(*args,**kwargs)
    else:
      m_infos = self.db.query("select id,title from blogs")
      self.render("index.html",m_infos = m_infos,user = self.current_user)

  def _info_action(self,*args,**kwargs):
    blog_id = self.get_argument('id',default="")
    blog_title_content = self.db.query("select title,content from blogs where id={0}".format(blog_id))
    self.render("editblog.html",user=self.current_user,blog_id=blog_id,blog_title=blog_title_content[0]['title'],blog_content=blog_title_content[0]['content'])
  
  
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
      self.db.execute("update blogs set title='{0}',content='{1}' where id='{2}'".format(blog_title,blog_content,blog_id))
      self.json("success",blog_title)
    except Exception as e:
      self.json("error",str(e))


  def _delete_blog_action(self):
    blog_id = self.get_argument("blog_id",default="")
    try:
      #db.delete_blog_content(id=blog_id)
      self.db.execute("delete from blogs where id={0}".format(blog_id))
      self.json("success",'ok')
    except Exception as e:
      self.json("error",str(e))