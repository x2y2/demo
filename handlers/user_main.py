#!/usr/bin/env python
#coding=utf-8
from base import BaseHandler

class UserBaseHandler(BaseHandler):
  user_infos = dict()

  #登录用户信息
  def login_user_infos(self):
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      UserBaseHandler.user_infos['login_user_id'] = login_user_info[0]['uid']
      UserBaseHandler.user_infos['login_user_pic'] = login_user_info[0]['pic']
      UserBaseHandler.user_infos['login_user'] = self.current_user
    else:
      UserBaseHandler.user_infos['login_user_id'] = None
      UserBaseHandler.user_infos['login_user_pic'] = None
      UserBaseHandler.user_infos['login_user'] = None


  #作者信息
  def author_infos(self):
    author_id = self.id
    author_info = self.db.query("SELECT username,pic FROM user WHERE uid=%s",author_id)
    UserBaseHandler.user_infos['author_id'] = self.id
    UserBaseHandler.user_infos['author_name'] = author_info[0]['username']
    UserBaseHandler.user_infos['author_pic'] = author_info[0]['pic']

  #作者的关注用户数
  def following_counts(self):
    author_id = self.id
    if self.redis.exists('following_count_' + author_id):
      following_count = self.redis.get('following_count_' + author_id)
    else:
      following_count = self.db.query('''SELECT count(to_user_id) count 
                                         FROM relation 
                                         WHERE from_user_id=%s''',author_id)[0]['count']
      self.redis.set('following_count_' + author_id,following_count)
    UserBaseHandler.user_infos['following_count'] = following_count

  #作者的文章数
  def count_articles(self):
    author_id = self.id
    if self.redis.exists('article_count_' + author_id):
      count_article = self.redis.get('article_count_' + author_id)
    else:
      count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",author_id)[0]['count']
      self.redis.set('article_count_' + author_id,count_article)
    UserBaseHandler.user_infos['count_article'] = count_article

  #作者的粉丝数
  def follower_counts(self):
    author_id = self.id
    if self.redis.exists('follower_count_' + author_id):
      follower_count = self.redis.get('follower_count_' + author_id)
    else:
      follower_count = self.db.query('''SELECT count(from_user_id) count 
                                        FROM relation 
                                        WHERE to_user_id=%s''',author_id)[0]['count']
      self.redis.set('follower_count_' + author_id,follower_count)
    UserBaseHandler.user_infos['follower_count'] = follower_count

  #登录用户是否已经关注过该作者
  def followeds(self):
    author_id = self.id
    followed = False
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("SELECT id FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,author_id)
      if len(id) == 0:
        followed = False
      else:
        followed = True
    UserBaseHandler.user_infos['followed'] = followed

  #共同的关注用户
  def common_ids(self):
    author_id = self.id
    common_id =[]
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      common_follower_id = self.db.query('''SELECT to_user_id 
                                            FROM relation 
                                            WHERE to_user_id in (
                                                  SELECT to_user_id 
                                                  FROM relation  
                                                  WHERE  from_user_id=%s) 
                                            AND from_user_id=%s''',author_id,current_user_id)
      for c_follower_id in common_follower_id:
        common_id.append(c_follower_id['to_user_id'])
    UserBaseHandler.user_infos['common_id'] = common_id

  #个人用户信息
  def personal_infos(self):
    personal_info = self.db.query('''SELECT gender,webchat_code,personal_profile 
                                  FROM user_info 
                                  WHERE user_uid=%s''',self.id)
    if personal_info:
      UserBaseHandler.user_infos['gender'] = personal_info[0]['gender']
      UserBaseHandler.user_infos['personal_profile'] = personal_info[0]['personal_profile']
      UserBaseHandler.user_infos['webchat_code'] = personal_info[0]['webchat_code']
    else:
      UserBaseHandler.user_infos['gender'] = None
      UserBaseHandler.user_infos['personal_profile'] = None
      UserBaseHandler.user_infos['webchat_code'] = None
