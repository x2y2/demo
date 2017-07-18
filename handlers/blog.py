#!/usr/bin/env python
#coding=utf8

from base import BaseHandler
import sys
import datetime
import hashlib
import markdown2
import HTMLParser


reload(sys)
sys.setdefaultencoding('utf8')

class BlogContentHandler(BaseHandler):
  def get(self):
    #登录用户信息
    if self.current_user is not None:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None
    bid = self.id
    b_infos = self.db.query('''SELECT 
                                  u.uid,
                                  u.pic,
                                  a.aid,
                                  a.user_name,
                                  a.title,
                                  a.content,
                                  a.created_at 
                                FROM articles a,user u 
                                WHERE 
                                  a.user_uid=u.uid 
                                AND 
                                  a.aid=%s
                            ''',bid
                            )
    c_infos = b_infos[0]['content']
    c_infos_html = markdown2.markdown(c_infos)
    html_parser = HTMLParser.HTMLParser()
    html = html_parser.unescape(c_infos_html)
    self.render("blog.html",
                b_infos=b_infos,
                c_infos_html= html,
                login_user=login_user,
                login_user_id=login_user_id,
                login_user_pic=login_user_pic)

class NewBlogHandler(BaseHandler):
  def get(self,*args,**kwargs):
    if self.current_user is not None:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None

    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)(login_user,login_user_id,login_user_pic)
    else:
      m_infos = self.db.query("select id,title from articles")
      self.render("index.html",m_infos = m_infos,login_user=login_user,login_user_id=login_user_id,login_user_pic=login_user_pic)

  def _info_action(self,login_user,login_user_id,login_user_pic):
    self.render("newblog.html",login_user=login_user,login_user_id=login_user_id,login_user_pic=login_user_pic)

  def post(self,*args,**kwargs):
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)()
    else:
      self.json("fail","no aciton!")

  def _add_blog_action(self):
    blog_title = self.get_argument("blog_title",default="")
    blog_content = self.get_argument("blog_content",default="")
    user_name = self.current_user
    created_at = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
    str = ''.join([created_at,user_name])
    str_md5 = hashlib.md5(str).hexdigest()
    blog_id = str_md5[0:16]
    try:
      self.db.execute('''INSERT INTO articles
                          (aid,
                           user_uid,
                           user_name,
                           title,
                           content,
                           created_at
                           )
                           VALUES
                           (%s,
                           (SELECT uid FROM user WHERE username=%s),
                           %s,%s,%s,%s
                           )''',
                           blog_id,
                           user_name,
                           user_name,
                           blog_title,
                           blog_content,
                           created_at)
      self.json("success",blog_id)
    except Exception as e:
      self.json('error',str(e))

class EditBlogHandler(BaseHandler):
  def get(self,*args,**kwargs):
    if self.current_user is not None:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None

    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)(login_user,login_user_id,login_user_pic)
    else:
      m_infos = self.db.query("select aid,title from articles")
      self.render("index.html",
                   m_infos = m_infos,
                   login_user=login_user,
                   login_user_id=login_user_id,
                   login_user_pic=login_user_pic)

  def _info_action(self,login_user,login_user_id,login_user_pic):
    blog_id = self.get_argument('id',default="")
    blog_title_content = self.db.query("select title,content from articles where aid=%s",blog_id)
    self.render("editblog.html",
                 login_user=login_user,
                 login_user_id=login_user_id,
                 login_user_pic=login_user_pic,
                 blog_id=blog_id,
                 blog_title=blog_title_content[0]['title'],
                 blog_content=blog_title_content[0]['content'])
  
  
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
      self.db.execute("update articles set title=%s,content=%s where aid=%s",blog_title,blog_content,blog_id)
      self.json("success",blog_title)
    except Exception as e:
      self.json("error",str(e))


  def _delete_blog_action(self):
    blog_id = self.get_argument("blog_id",default="")
    try:
      self.db.execute("delete from articles where aid=%s",blog_id)
      uid = self.db.query("select uid from user where username=%s",self.current_user)[0]['uid']
      self.json("success",uid)
    except Exception as e:
      self.json("error",str(e))



    