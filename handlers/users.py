#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
import hashlib
import urlparse
import json

class UsersHandler(BaseHandler):
  def get(self):
    uid = author_id = self.id
    #登录用户信息
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None
    #作者信息
    author_name = self.db.query("select username from user where uid=%s",uid)[0]['username']
    author_pic = self.db.query("SELECT pic FROM user WHERE uid=%s",uid)[0]['pic']
    #作者的文章数
    count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",uid)[0]['count']
    #登录用户是否已经关注过该作者
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("select id from relation where from_user_id=%s and to_user_id=%s and type='2'",current_user_id,author_id)
      if len(id) == 0:
        follower = False
      else:
        follower = True
    else:
      follower = False
    #作者的关注用户数
    if self.redis.exists('following_count_' + author_id):
      following_count = self.redis.get('following_count_' + author_id)
    else:
      following_count = self.db.query('''SELECT count(to_user_id) count 
                                         FROM relation 
                                         WHERE from_user_id=%s''',author_id)[0]['count']
      self.redis.set('following_count_' + author_id,following_count)
    #作者的粉丝数
    if self.redis.exists('follower_count_' + author_id):
      follower_count = self.redis.get('follower_count_' + author_id)
    else:
      follower_count = self.db.query('''SELECT count(from_user_id) count 
                                        FROM relation 
                                        WHERE to_user_id=%s''',author_id)[0]['count']
      self.redis.set('follower_count_' + author_id,follower_count)
    #获取URL参数
    string = self.get_argument("order_by",default="")
    action = "_%s" % string
    if hasattr(self,action):
      getattr(self,action)(count_article,uid,author_name,author_pic,author_id,
                           login_user_pic,login_user_id,login_user,
                           follower,follower_count,following_count)
    else:
      self.user_info(count_article,author_name,author_pic,author_id,
                     login_user_pic,login_user_id,login_user,
                     follower,follower_count,following_count)

  #用户动态信息
  def user_info(self,count_article,author_name,author_pic,author_id,
                login_user_pic,login_user_id,login_user,
                follower,follower_count,following_count):  
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
                  login_user_pic,login_user_id,login_user,
                  follower,follower_count,following_count):
    m_infos = self.db.query('''SELECT u.uid,u.pic,u.username,a.aid,a.title,a.content,a.created_at,a.comment_count,a.read_count 
                               FROM articles a,user u 
                               WHERE a.user_uid=u.uid 
                               AND a.user_uid=%s
                               ORDER BY created_at
                               DESC
                            ''',
                            suid
                            )

    self.render("users.html",
                 author_name=self.author_name,
                 author_pic=self.author_pic,
                 author_id=self.author_id,
                 m_infos=self.m_infos,
                 uid=self.uid,
                 count_article=self.count_article,
                 login_user_pic=self.login_user_pic,
                 login_user_id=self.login_user_id,
                 login_user=self.login_user,
                 follower=self.follower,
                 follower_count=self.follower_count,
                 following_count=self.following_count)
  #按最新评论排序显示文章
  def _commented_at(self,count_article,uid,author_name,author_pic,author_id,
                    login_user_pic,login_user_id,login_user,
                    follower,follower_count,following_count):
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
           login_user_pic,login_user_id,login_user,
           follower,follower_count,following_count):
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

#关注用户类
class FollowHandler(BaseHandler):
  def get(self):
    uid = self.id
    #作者姓名
    author_name = self.db.query("select username from user where uid=%s",uid)[0]['username']
    count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",uid)[0]['count']
    #登录用户信息
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None
    #作者信息
    author_info = self.db.query("SELECT pic FROM user WHERE uid=%s",uid)
    author_pic = author_info[0]['pic']
    author_id = uid
    
    #是否已经关注
    user_id = self.id
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query('''SELECT id 
                            FROM relation 
                            WHERE from_user_id=%s 
                            AND to_user_id=%s 
                            AND type=\'2\'''',current_user_id,user_id)
      if len(id) == 0:
        follower = False
      else:
        follower = True
    else:
      follower = False
    
    #共同的关注用户
    user_id = uid
    common_id =[]
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      common_follower_id = self.db.query('''SELECT to_user_id 
                                            FROM relation 
                                            WHERE to_user_id in (
                                                  SELECT to_user_id 
                                                  FROM relation  
                                                  WHERE  from_user_id=%s) 
                                            AND from_user_id=%s''',user_id,current_user_id)
      for c_follower_id in common_follower_id:
        common_id.append(c_follower_id['to_user_id'])

    #根据URI最后的关键字选择执行方法
    string = self.arg
    action = "_%s" % string
    if hasattr(self,action):
      getattr(self,action)(count_article,uid,
                           author_name,author_pic,author_id,
                           login_user_pic,login_user_id,login_user,
                           follower,common_id)
    else:
      pass

  def _following(self,count_article,uid,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user,follower,common_id):
    user_id = self.id
    #获取作者关注的用户信息
    f_infos = self.db.query('''SELECT r.from_user_id,u.uid,u.username,u.pic 
                               FROM relation r,user u  
                               WHERE u.uid=r.to_user_id 
                               AND r.from_user_id=%s''',user_id)
    #该用户的关注数
    if self.redis.exists('following_count_' + user_id):
      following_count = self.redis.get('following_count_' + user_id)
    else:
      following_count = self.db.query("SELECT count(to_user_id) count FROM relation WHERE from_user_id=%s",user_id)[0]['count']
      self.redis.set('following_count_' + user_id,following_count)
    #关注用户的关注数
    following_u_counts = self.db.query('''SELECT t.uid,r.to_user_id  
                                          FROM (SELECT r.from_user_id,u.uid 
                                                FROM relation r,user u  
                                                WHERE u.uid=r.to_user_id  
                                                AND r.from_user_id=%s) as t 
                                          LEFT JOIN relation r 
                                          ON t.uid=r.from_user_id''',user_id)
    dic_following = {}
    for following_u_count in following_u_counts:
      dic_following[following_u_count['uid']] = 0

    for following_u_count in following_u_counts:
      if following_u_count['to_user_id'] is not None:
        dic_following[following_u_count['uid']] += 1

    #该用户粉丝数
    if self.redis.exists('follower_count_' + user_id):
      follower_count = self.redis.get('follower_count_' + user_id)
    else:
      follower_count = self.db.query("SELECT count(from_user_id) count FROM relation WHERE to_user_id=%s",user_id)[0]['count']
      self.redis.set('follower_count_' + user_id,follower_count)
    #关注用户的粉丝数
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

    #关注用户的文章数
    articles_u_counts = self.db.query('''SELECT t.uid,a.aid 
                                         FROM (SELECT r.from_user_id,u.uid 
                                               FROM relation r,user u 
                                               WHERE u.uid=r.to_user_id 
                                               AND r.from_user_id=%s) as t 
                                         LEFT JOIN articles a 
                                         ON a.user_uid=t.uid''',user_id)
    dic_articles = {}
    for articles_u_count in articles_u_counts:
      dic_articles[articles_u_count['uid']] = 0

    for articles_u_count in articles_u_counts:
      if articles_u_count['aid'] is not None:
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
                 dic_articles=dic_articles)


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
  def _following_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.id
    try:
      self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,user_id)
      self.redis.incr('following_count_' + current_user_id)
      self.json('success','/users/' + user_id)
    except Exception as e:
      self.json('error',e)

  #将作者的关注用户添加为自己的关注用户
  def _following_u_add_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    try:
      self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,user_id)
      self.redis.incr('following_count_' + current_user_id)
      self.json('success','/users/' + self.id)
    except Exception as e:
      self.json('error',e)

  #将作者从关注用户中删除
  def _following_remove_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.id
    try:
      self.db.execute("DELETE FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,user_id)
      self.redis.decr('following_count_'+ current_user_id)
      self.json('success','/users/' + self.id)
    except Exception as e:
      self.json('error',e)

  #从我的关注列表中取消关注
  def _following_u_remove_action(self):
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    user_id = self.get_argument("user_id",default="")
    try:
      self.db.execute("DELETE FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,user_id)
      self.redis.decr('following_count_' + current_user_id)
      self.json('success','/users/' + self.id)
    except Exception as e:
      self.json('error',e)

class FollowersHandler(BaseHandler):
  def get(self):
    uid = self.id
    author_name = self.db.query("select username from user where uid=%s",uid)[0]['username']
    count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",uid)[0]['count']
    #登录用户信息
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None
    #作者信息
    author_info = self.db.query("SELECT pic FROM user WHERE uid=%s",uid)
    author_pic = author_info[0]['pic']
    author_id = uid
    #是否已经关注
    if self.current_user:
      user_id = self.id
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
    common_id =[]
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      common_follower_id = self.db.query('''SELECT to_user_id 
                                            FROM relation 
                                            WHERE to_user_id in (
                                                  SELECT from_user_id 
                                                  FROM relation 
                                                  WHERE to_user_id=%s) 
                                            AND from_user_id=%s''',user_id,current_user_id)
      for c_follower_id in common_follower_id:
        common_id.append(c_follower_id['to_user_id'])
    #根据URI最后的关键字选择执行方法
    string = self.arg
    action = "_%s" % string
    if hasattr(self,action):
      getattr(self,action)(count_article,uid,
                           author_name,author_pic,author_id,
                           login_user_pic,login_user_id,login_user,
                           follower,common_id)
    else:
      pass
  
  def _followers(self,count_article,uid,author_name,author_pic,author_id,login_user_pic,login_user_id,login_user,follower,common_id):
    user_id = self.id
    #获取作者的关注用户信息
    f_infos = self.db.query('''SELECT r.to_user_id,u.uid,u.username,u.pic 
                               FROM relation r,user u  
                               WHERE u.uid=r.from_user_id 
                               AND r.to_user_id=%s''',user_id)
    #该用户的关注数
    if self.redis.exists('following_count_' + user_id):
      following_count = self.redis.get('following_count_' + user_id)
    else:
      following_count = self.db.query("SELECT count(to_user_id) count FROM relation WHERE from_user_id=%s",user_id)[0]['count']
      self.redis.set('following_count_' + user_id,following_count)
    #该用户粉丝数
    if self.redis.exists('follower_count_' + user_id):
      follower_count = self.redis.get('follower_count_' + user_id)
    else:
      follower_count = self.db.query("SELECT count(from_user_id) count FROM relation WHERE to_user_id=%s",user_id)[0]['count']
      self.redis.set('follower_count_' + user_id,follower_count)
    #粉丝的关注用户数
    follower_u_counts = self.db.query('''SELECT from_user_id,count(from_user_id) count 
                                        FROM relation 
                                        WHERE from_user_id IN
                                           (SELECT from_user_id 
                                            FROM relation 
                                            WHERE to_user_id=%s) 
                                        GROUP BY from_user_id''',user_id)
    dic_follower = {}
    for follower_u_count in follower_u_counts:
      dic_follower[follower_u_count['from_user_id']] = follower_u_count['count']

    #粉丝的粉丝数
    follower_f_counts = self.db.query('''SELECT t.from_user_id tfrom,r.from_user_id rfrom 
                                        FROM  (SELECT from_user_id,to_user_id 
                                               FROM relation 
                                               WHERE to_user_id=%s) as t  
                                        LEFT JOIN relation r 
                                        ON t.from_user_id=r.to_user_id''',user_id)
    dic_follower_f = {}
    for follower_f_count in follower_f_counts:
      dic_follower_f[follower_f_count['tfrom']] = 0

    for follower_f_count in follower_f_counts:
      if follower_f_count['rfrom'] is not None:
        dic_follower_f[follower_f_count['tfrom']] += 1

    #粉丝的文章数
    follower_article_counts = self.db.query('''SELECT t.from_user_id,a.aid 
                                              FROM (SELECT from_user_id,to_user_id 
                                                    FROM relation 
                                                    WHERE to_user_id=%s) as t 
                                              LEFT JOIN articles a 
                                              ON t.from_user_id=a.user_uid''',user_id)
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
                 dic_follower_a=dic_follower_a)

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
      self.json('success','取消成功')
    except Exception as e:
      self.json('error',e)
