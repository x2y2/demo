#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
import hashlib
import urlparse
import json

class UsersHandler(BaseHandler):
  def get(self):
    uid = self.id
    if uid is None: 
      author_name = self.current_user
      count_article = self.db.query('''SELECT COUNT(*) count FROM articles WHERE  (select uid from user where username=%s)''',self.current_user)[0]['count']
    else:
      author_name = self.db.query("select username from user where uid=%s",uid)[0]['username']
      count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",uid)[0]['count']
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
    #是否已经关注
    user_id = self.id
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("select id from relation where from_user_id=%s and to_user_id=%s and type='2'",current_user_id,user_id)
      if len(id) == 0:
        follower = False
      else:
        follower = True
    else:
      follower = False
    #该用户的关注用户数
    following_count = self.db.query("select count(to_user_id) count from relation where from_user_id=%s;",user_id)[0]['count']
    #该用户粉丝数
    follower_count = self.db.query("select count(from_user_id) count from relation where to_user_id=%s;",user_id)[0]['count']

    #获取URL参数
    string = self.get_argument("order_by",default="")
    action = "_%s" % string
    if hasattr(self,action):
      getattr(self,action)(count_article,uid,author_name,author_pic,author_id,
                           login_user_pic,login_user_id,login_user,follower,follower_count,following_count)
    else:
      self.user_info(count_article,author_name,author_pic,author_id,
                     login_user_pic,login_user_id,login_user,follower,follower_count,following_count)

  #用户动态信息
  def user_info(self,count_article,author_name,author_pic,author_id,
                login_user_pic,login_user_id,login_user,follower,follower_count,following_count):  
    self.render("user_info.html",
                 author_name=author_name,
                 login_user=self.current_user,
                 login_user_pic=login_user_pic,
                 login_user_id=login_user_id,
                 author_pic = author_pic,
                 author_id = author_id,
                 count_article=count_article,
                 follower=follower,
                 follower_count=follower_count,
                 following_count=following_count)
  #文章
  def _created_at(self,count_article,uid,author_name,author_pic,author_id,
                  login_user_pic,login_user_id,login_user,follower,follower_count,following_count):
    m_infos = self.db.query('''SELECT u.uid,u.pic,u.username,a.aid,a.title,a.content,a.created_at,a.comment_count,a.read_count 
                               FROM articles a,user u 
                               WHERE a.user_uid=u.uid 
                               AND a.user_uid=%s
                               ORDER BY created_at
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
                 login_user=login_user,
                 follower=follower,
                 follower_count=follower_count,
                 following_count=following_count)
  #按最新评论排序显示文章
  def _commented_at(self,count_article,uid,author_name,author_pic,author_id,
                    login_user_pic,login_user_id,login_user,follower,follower_count,following_count):
    comment_infos = self.db.query('''SELECT a.aid,a.user_uid uid,u.username,u.pic,a.title,a.created_at,a.comment_count,a.read_count 
                                     FROM comments c,articles a,user u
                                     WHERE c.article_aid=a.aid 
                                     AND a.user_uid=u.uid
                                     AND a.user_uid=%s
                                     GROUP BY a.title 
                                     ORDER BY c.comment_time 
                                     DESC''',uid)
 
    self.render("commented.html",
                 author_name=author_name,
                 author_pic=author_pic,
                 author_id=author_id,
                 count_article=count_article,
                 login_user_pic=login_user_pic,
                 login_user_id=login_user_id,
                 login_user=login_user,
                 comment_infos=comment_infos,
                 follower=follower,
                 follower_count=follower_count,
                 following_count=following_count)

  #显示热门文章
  def _top(self,count_article,uid,author_name,author_pic,author_id,
           login_user_pic,login_user_id,login_user,follower,follower_count,following_count):
    hot_infos = self.db.query('''SELECT a.aid,a.user_uid uid,u.username,u.pic,a.title,a.created_at,a.comment_count,a.read_count 
                                 FROM comments c,articles a,user u
                                 WHERE c.article_aid=a.aid 
                                 AND a.user_uid=u.uid
                                 AND a.user_uid=%s
                                 GROUP BY a.title 
                                 ORDER BY a.read_count
                                 DESC''',uid)
    self.render("hot.html",
               author_name=author_name,
               author_pic=author_pic,
               author_id=author_id,
               count_article=count_article,
               login_user_pic=login_user_pic,
               login_user_id=login_user_id,
               login_user=login_user,
               hot_infos=hot_infos,
               follower=follower,
               follower_count=follower_count,
               following_count=following_count)

class FollowHandler(BaseHandler):
  def get(self):
    #url = self.request.uri
    #ret = urlparse.urlparse(url)
    #path = ret.path
    #uid = path.split('/')[2]
    uid = self.id
    #作者姓名
    if uid is None: 
      author_name = self.current_user
      count_article = self.db.query('''SELECT COUNT(*) count FROM articles WHERE  user_name=%s''',self.current_user)[0]['count']
    else:
      author_name = self.db.query("select username from user where uid=%s",uid)[0]['username']
      count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",uid)[0]['count']
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
    
    #是否已经关注
    user_id = uid
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("select id from relation where from_user_id=%s and to_user_id=%s and type='2'",current_user_id,user_id)
      if len(id) == 0:
        follower = False
      else:
        follower = True
    else:
      follower = False
    
    #共同的关注用户
    user_id = uid
    #将共同的关注用户id存入列表
    common_id =[]
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      common_follower_id = self.db.query('''select to_user_id 
                     from relation 
                     where to_user_id in (
                            select r.to_user_id 
                            from relation r,user u  
                            where u.uid=r.to_user_id 
                            and r.from_user_id=%s) 
                     and from_user_id=%s''',user_id,current_user_id)
      for c_follower_id in common_follower_id:
        common_id.append(c_follower_id['to_user_id'])

    #根据URL选择执行方法
    url = self.request.uri
    ret = urlparse.urlparse(url)
    path = ret.path
    
    string = path.split('/')[-1]
    action = "_%s" % string
    if hasattr(self,action):
      getattr(self,action)(count_article,uid,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user,path,follower,common_id)
    else:
      pass

  def _following(self,count_article,uid,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user,path,follower,common_id):
    user_id = path.split('/')[-2]
    #获取用户信息
    f_infos = self.db.query('''SELECT r.from_user_id,u.uid,u.username,u.pic 
                               FROM relation r,user u  
                               WHERE u.uid=r.to_user_id 
                               AND r.from_user_id=%s''',user_id)
    #该用户的关注用户数
    following_count = self.db.query("select count(to_user_id) count from relation where from_user_id=%s",user_id)[0]['count']
    #该用户关注用户的关注用户数
    following_u_counts = self.db.query('''SELECT from_user_id,count(from_user_id) count
                                       FROM relation 
                                       WHERE from_user_id in (
                                            SELECT u.uid 
                                            FROM relation r,user u 
                                            WHERE u.uid=r.to_user_id  
                                            AND r.from_user_id=%s) 
                                       GROUP BY from_user_id''',user_id)
    dic_following = {}
    for following_u_count in following_u_counts:
      dic_following[following_u_count['from_user_id']] = following_u_count['count']

    #该用户粉丝数
    follower_count = self.db.query("select count(from_user_id) count from relation where to_user_id=%s",user_id)[0]['count']
    #该用户关注用户的粉丝数
    follower_u_counts = self.db.query('''SELECT to_user_id,count(to_user_id) count 
                                         FROM relation 
                                         WHERE to_user_id in (
                                               SELECT u.uid 
                                               FROM relation r,user u 
                                               WHERE u.uid=r.to_user_id 
                                               AND r.from_user_id=%s)  
                                               GROUP BY to_user_id''',user_id)
    dic_follower = {}
    for follower_u_count in follower_u_counts:
      dic_follower[follower_u_count['to_user_id']] = follower_u_count['count']

    self.render('following.html',
                 f_infos=f_infos,
                 count_article=count_article,
                 author_name=author_name,
                 author_pic=author_pic,
                 author_id=author_id,
                 login_user_pic=login_user_pic,
                 login_user_id=login_user_id,
                 login_user=login_user,
                 follower=follower,
                 common_id=common_id,
                 follower_count=follower_count,
                 following_count=following_count,
                 dic_following = dic_following,
                 dic_follower = dic_follower)


  def post(self):
    url = self.get_argument("url",default="")
    string = url.split('/')[-1]
    action = "_%s_action" % string

    if self.current_user:
      if hasattr(self,action):
        getattr(self,action)()
      else:
        self.json("fail","no aciton!")
    else:
      self.json('login','/login')

  #添加作者为关注用户
  def _follower_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.id
    try:
      self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,user_id)
      #self.redirect('/users/' + user_id)
      self.json('success','/users/' + user_id + '/following')
    except Exception as e:
      self.json('error',e)

  #将作者的关注用户添加为自己的关注用户
  def _follower_u_add_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    try:
      self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,user_id)
      self.json('success','/users/' + self.id + '/following')
    except Exception as e:
      self.json('error',e)

  #将作者从关注用户中删除
  def _follower_remove_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.id
    try:
      self.db.execute("delete from relation where from_user_id=%s and to_user_id=%s and type='2'",current_user_id,user_id)
      self.json('success','/users/' + self.id + '/following')
    except Exception as e:
      self.json('error',e)

  #将作者的关注用户从我的关注列表中删除
  def _follower_u_remove_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    try:
      self.db.execute("delete from relation where from_user_id=%s and to_user_id=%s and type='2'",current_user_id,user_id)
      self.json('success','/users/' + self.id + '/following')
    except Exception as e:
      self.json('error',e)

