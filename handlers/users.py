#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
from user_main import UserBaseHandler
import hashlib
import urlparse
import json
import HTMLParser
import ujson

class ArticlesHandler(UserBaseHandler):
  def get(self):
    if self.login_user_info:
      login_user_id = self.login_user_info[0]['uid']
      login_user_pic = self.login_user_info[0]['pic']
    else:
      login_user_id = self.login_user_info
      login_user_pic = self.login_user_info
    login_user = self.current_user
    author_id = self.id
    author_name = self.author_info[0]['username']
    author_pic = self.author_info[0]['pic']
    count_article = self.count_article
    follower_count = self.follower_count
    following_count = self.following_count
    follower = self.followed
    if self.personal_info:
      gender = self.personal_info[0]['gender']
      personal_profile = self.personal_info[0]['personal_profile']
      webchat_code = self.personal_info[0]['webchat_code']
    else:
      gender = personal_profile = webchat_code = None

    #根据URL选择执行方法
    url = self.get_argument("order_by",default="")
    action = "_%s" % url
    if hasattr(self,action):
      getattr(self,action)(count_article,
                           author_name,author_pic,author_id,
                           login_user_pic,login_user_id,login_user,
                           follower,follower_count,following_count,
                           gender,personal_profile,webchat_code)
    else:
      self.user_info(count_article,author_name,author_pic,author_id,
                     login_user_pic,login_user_id,login_user,
                     follower,follower_count,following_count,
                     gender,personal_profile,webchat_code)

  #用户动态信息
  def user_info(self,count_article,author_name,author_pic,author_id,
                login_user_pic,login_user_id,login_user,
                follower,follower_count,following_count,
                gender,personal_profile,webchat_code):  
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
                 following_count=following_count,
                 gender=gender,
                 personal_profile=personal_profile,
                 webchat_code=webchat_code)
  #按发布时间展示文章
  def _created_at(self,count_article,author_name,author_pic,author_id,
                  login_user_pic,login_user_id,login_user,
                  follower,follower_count,following_count,
                  gender,personal_profile,webchat_code):
    m_infos = self.db.query('''SELECT u.uid,u.pic,u.username,a.aid,a.title,a.content,a.created_at,a.comment_count,a.read_count 
                               FROM articles a,user u 
                               WHERE a.user_uid=u.uid 
                               AND a.user_uid=%s
                               ORDER BY created_at
                               DESC
                            ''',author_id)

    self.render("users.html",
                 author_name=author_name,
                 author_pic=author_pic,
                 author_id=author_id,
                 m_infos=m_infos,
                 count_article=count_article,
                 login_user_pic=login_user_pic,
                 login_user_id=login_user_id,
                 login_user=login_user,
                 follower=follower,
                 follower_count=follower_count,
                 following_count=following_count,
                 gender=gender,
                 personal_profile=personal_profile,
                 webchat_code=webchat_code)
  #按最新评论显示文章
  def _commented_at(self,count_article,author_name,author_pic,author_id,
                    login_user_pic,login_user_id,login_user,
                    follower,follower_count,following_count,
                    gender,personal_profile,webchat_code):
    comment_infos = self.db.query('''SELECT a.aid,a.user_uid uid,u.username,u.pic,a.title,a.created_at,a.comment_count,a.read_count 
                                     FROM comments c,articles a,user u
                                     WHERE c.article_aid=a.aid 
                                     AND a.user_uid=u.uid
                                     AND a.user_uid=%s
                                     GROUP BY a.title 
                                     ORDER BY c.comment_time 
                                     DESC''',author_id)
 
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
                 following_count=following_count,
                 gender=gender,
                 personal_profile=personal_profile,
                 webchat_code=webchat_code)

  #显示热门文章
  def _top(self,count_article,author_name,author_pic,author_id,
           login_user_pic,login_user_id,login_user,
           follower,follower_count,following_count,
           gender,personal_profile,webchat_code):
    hot_infos = self.db.query('''SELECT a.aid,a.user_uid uid,u.username,u.pic,a.title,a.created_at,a.comment_count,a.read_count 
                                 FROM comments c,articles a,user u
                                 WHERE c.article_aid=a.aid 
                                 AND a.user_uid=u.uid
                                 AND a.user_uid=%s
                                 GROUP BY a.title 
                                 ORDER BY a.read_count
                                 DESC''',author_id)
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
               following_count=following_count,
               gender=gender,
               personal_profile=personal_profile,
               webchat_code=webchat_code)

  def post(self,*args,**kwargs):
    action = self.arg
    action = "_%s_action" % action
    if hasattr(self,action):
      getattr(self,action)()
    else:
      self.json("fail","no action")

  def _personal_profile_save_action(self):
    personal_profile = self.get_argument('personal_profile',default='')
    try:
      self.db.execute('''UPDATE user_info 
                        SET personal_profile=%s 
                        WHERE user_uid 
                        IN (SELECT uid 
                            FROM user 
                            WHERE username=%s)''',personal_profile,self.current_user)
      self.json('success','ok')
    except Exception as e:
      self.json('error',e)

#关注用户
class FollowingHandler(UserBaseHandler):
  def get(self):
    if self.login_user_info:
      login_user_id = self.login_user_info[0]['uid']
      login_user_pic = self.login_user_info[0]['pic']
    else:
      login_user_id = self.login_user_info
      login_user_pic = self.login_user_info
    login_user = self.current_user
    author_id = self.id
    author_name = self.author_info[0]['username']
    author_pic = self.author_info[0]['pic']
    count_article = self.count_article
    follower_count = self.follower_count
    following_count = self.following_count
    follower = self.followed
    common_id = self.common_id
    if self.personal_info:
      gender = self.personal_info[0]['gender']
      personal_profile = self.personal_info[0]['personal_profile']
      webchat_code = self.personal_info[0]['webchat_code']
    else:
      gender = personal_profile = webchat_code = None
    #根据URI选择执行方法
    url = self.arg
    action = "_%s" % url
    if hasattr(self,action):
      getattr(self,action)(count_article,
                           author_name,author_pic,author_id,
                           login_user_pic,login_user_id,login_user,
                           follower,following_count,follower_count,common_id,
                           gender,personal_profile,webchat_code)
    else:
      pass

  def _following(self,count_article,author_name,author_pic,author_id,
                 login_user_pic,login_user_id,login_user,
                 follower,following_count,follower_count,common_id,
                 gender,personal_profile,webchat_code):
    #获取作者关注的用户信息
    f_infos = self.db.query('''SELECT r.from_user_id,u.uid,u.username,u.pic 
                               FROM relation r,user u  
                               WHERE u.uid=r.to_user_id 
                               AND r.from_user_id=%s''',author_id)
    #关注用户的关注数
    following_u_counts = self.db.query('''SELECT t.uid,r.to_user_id  
                                          FROM (SELECT r.from_user_id,u.uid 
                                                FROM relation r,user u  
                                                WHERE u.uid=r.to_user_id  
                                                AND r.from_user_id=%s) as t 
                                          LEFT JOIN relation r 
                                          ON t.uid=r.from_user_id''',author_id)
    dic_following = {}
    for following_u_count in following_u_counts:
      dic_following[following_u_count['uid']] = 0

    for following_u_count in following_u_counts:
      if following_u_count['to_user_id']:
        dic_following[following_u_count['uid']] += 1
    
    #关注用户的粉丝数
    follower_u_counts = self.db.query('''SELECT to_user_id,count(to_user_id) count 
                                         FROM relation 
                                         WHERE to_user_id in (
                                               SELECT u.uid 
                                               FROM relation r,user u 
                                               WHERE u.uid=r.to_user_id 
                                               AND r.from_user_id=%s)  
                                               GROUP BY to_user_id''',author_id)
    dic_follower = {}
    for follower_u_count in follower_u_counts:
      dic_follower[follower_u_count['to_user_id']] = follower_u_count['count']
    #关注用户的文章数
    articles_u_counts = self.db.query('''SELECT t.uid,a.aid 
                                         FROM (SELECT r.from_user_id,u.uid 
                                               FROM relation r,user u 
                                               WHERE u.uid=r.to_user_id 
                                               AND r.from_user_id=%s) as t 
                                         LEFT JOIN articles a 
                                         ON a.user_uid=t.uid''',author_id)
    dic_articles = {}
    for articles_u_count in articles_u_counts:
      dic_articles[articles_u_count['uid']] = 0

    for articles_u_count in articles_u_counts:
      if articles_u_count['aid']:
        dic_articles[articles_u_count['uid']] += 1

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
                 dic_follower = dic_follower,
                 dic_articles=dic_articles,
                 gender=gender,
                 personal_profile=personal_profile,
                 webchat_code=webchat_code)


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

  #关注该作者
  def _following_add_action(self):
    author_id = self.id
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    try:
      self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,author_id)
      self.redis.incr('following_count_' + current_user_id)
      self.redis.incr('follower_count_' + author_id)
      self.json('success','/users/' + self.id)
    except Exception as e:
      self.json('error',e)

  #关注该作者的关注用户
  def _following_u_add_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    id = self.db.query("SELECT id FROM relation WHERE from_user_id=%s and to_user_id=%s and type='2'",current_user_id,user_id)
    if not id:
      try:
        self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,user_id)
        self.redis.incr('following_count_' + current_user_id)
        self.redis.incr('follower_count_' + user_id)
        self.json('success','/users/' + self.id)
      except Exception as e:
        self.json('error',e)

  #取消关注作者
  def _following_remove_action(self):
    author_id = self.id
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    try:
      self.db.execute("DELETE FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,author_id)
      self.redis.decr('following_count_'+ current_user_id)
      self.redis.decr('follower_count_'+ author_id)
      self.json('success','/users/' + self.id)
    except Exception as e:
      self.json('error',e)

  #取消关注作者的关注用户
  def _following_u_remove_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    try:
      self.db.execute("DELETE FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,user_id)
      self.redis.decr('following_count_' + current_user_id)
      self.redis.decr('follower_count_' + user_id)
      self.json('success','/users/' + self.id)
    except Exception as e:
      self.json('error',e)

class FollowersHandler(UserBaseHandler):
  def get(self):
    if self.login_user_info:
      login_user_id = self.login_user_info[0]['uid']
      login_user_pic = self.login_user_info[0]['pic']
    else:
      login_user_id = self.login_user_info
      login_user_pic = self.login_user_info
    login_user = self.current_user
    author_id = self.id
    author_name = self.author_info[0]['username']
    author_pic = self.author_info[0]['pic']
    count_article = self.count_article
    follower_count = self.follower_count
    following_count = self.following_count
    follower = self.followed
    common_id = self.common_id
    if self.personal_info:
      gender = self.personal_info[0]['gender']
      personal_profile = self.personal_info[0]['personal_profile']
      webchat_code = self.personal_info[0]['webchat_code']
    else:
      gender = personal_profile = webchat_code = None
    #根据URI最后的关键字选择执行方法
    string = self.arg
    action = "_%s" % string
    if hasattr(self,action):
      getattr(self,action)(count_article,
                           author_name,author_pic,author_id,
                           login_user_pic,login_user_id,login_user,
                           follower,following_count,follower_count,common_id,
                           gender,personal_profile,webchat_code)
    else:
      pass
  
  def _followers(self,count_article,author_name,author_pic,author_id,
                 login_user_pic,login_user_id,login_user,
                 follower,following_count,follower_count,common_id,
                 gender,personal_profile,webchat_code):
    #获取作者的关注用户信息
    f_infos = self.db.query('''SELECT r.to_user_id,u.uid,u.username,u.pic 
                               FROM relation r,user u  
                               WHERE u.uid=r.from_user_id 
                               AND r.to_user_id=%s''',author_id)
    #粉丝的关注用户数
    follower_u_counts = self.db.query('''SELECT from_user_id,count(from_user_id) count 
                                        FROM relation 
                                        WHERE from_user_id IN
                                           (SELECT from_user_id 
                                            FROM relation 
                                            WHERE to_user_id=%s) 
                                        GROUP BY from_user_id''',author_id)
    dic_follower = {}
    for follower_u_count in follower_u_counts:
      dic_follower[follower_u_count['from_user_id']] = follower_u_count['count']

    #粉丝的粉丝数
    follower_f_counts = self.db.query('''SELECT t.from_user_id tfrom,r.from_user_id rfrom 
                                        FROM  (SELECT from_user_id,to_user_id 
                                               FROM relation 
                                               WHERE to_user_id=%s) as t  
                                        LEFT JOIN relation r 
                                        ON t.from_user_id=r.to_user_id''',author_id)
    dic_follower_f = {}
    for follower_f_count in follower_f_counts:
      dic_follower_f[follower_f_count['tfrom']] = 0

    for follower_f_count in follower_f_counts:
      if follower_f_count['rfrom']:
        dic_follower_f[follower_f_count['tfrom']] += 1

    #粉丝的文章数
    follower_article_counts = self.db.query('''SELECT t.from_user_id,a.aid 
                                              FROM (SELECT from_user_id,to_user_id 
                                                    FROM relation 
                                                    WHERE to_user_id=%s) as t 
                                              LEFT JOIN articles a 
                                              ON t.from_user_id=a.user_uid''',author_id)
    dic_follower_a = {}
    for follower_article_count in follower_article_counts:
      dic_follower_a[follower_article_count['from_user_id']] = 0

    for follower_article_count in follower_article_counts:
      if follower_article_count['aid'] is not None:
        dic_follower_a[follower_article_count['from_user_id']] += 1

    self.render('followers.html',
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
                 following_count=following_count,
                 follower_count=follower_count,
                 dic_follower=dic_follower,
                 dic_follower_f=dic_follower_f,
                 dic_follower_a=dic_follower_a,
                 gender=gender,
                 personal_profile=personal_profile,
                 webchat_code=webchat_code)

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

  #将作者的粉丝添加到自己的关注列表
  def _follower_u_add_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    try:
      self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,user_id)
      self.redis.incr('following_count_' + current_user_id)
      self.redis.incr('follower_count_' + user_id)
      self.json('success','关注成功')
    except Exception as e:
      self.write(json.dumps({'error',e}))

  #取消关注作者的粉丝
  def _follower_u_remove_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    try:
      self.db.execute("DELETE FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,user_id)
      self.redis.decr('following_count_' + current_user_id)
      self.redis.decr('follower_count_' + user_id)
      self.json('success','取消成功')
    except Exception as e:
      self.json('error',e)
