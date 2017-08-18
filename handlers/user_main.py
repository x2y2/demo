#!/usr/bin/env python
#coding=utf-8
from base import BaseHandler

class UserBaseHandler(BaseHandler):
  #登录用户信息
  @property
  def login_user_info(self):
    author_id = self.id
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
    else:
      login_user_info = None
    return login_user_info

   #作者信息
  @property
  def author_info(self):
    author_id = self.id
    author_info = self.db.query("SELECT username,pic FROM user WHERE uid=%s",author_id)
    return author_info

  #作者的关注用户数
  @property
  def following_count(self):
    author_id = self.id
    if self.redis.exists('following_count_' + author_id):
      following_count = self.redis.get('following_count_' + author_id)
    else:
      following_count = self.db.query('''SELECT count(to_user_id) count 
                                         FROM relation 
                                         WHERE from_user_id=%s''',author_id)[0]['count']
      self.redis.set('following_count_' + author_id,following_count)
    return following_count

  #作者的文章数
  @property
  def count_article(self):
    author_id = self.id
    if self.redis.exists('article_count_' + author_id):
      count_article = self.redis.get('article_count_' + author_id)
    else:
      count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",author_id)[0]['count']
      self.redis.set('article_count_' + author_id,count_article)
    return count_article

  #作者的粉丝数
  @property
  def follower_count(self):
    author_id = self.id
    if self.redis.exists('follower_count_' + author_id):
      follower_count = self.redis.get('follower_count_' + author_id)
    else:
      follower_count = self.db.query('''SELECT count(from_user_id) count 
                                        FROM relation 
                                        WHERE to_user_id=%s''',author_id)[0]['count']
      self.redis.set('follower_count_' + author_id,follower_count)
    return follower_count

  #登录用户是否已经关注过该作者
  @property
  def followed(self):
    author_id = self.id
    followed = False
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("SELECT id FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,author_id)
      if len(id) == 0:
        followed = False
      else:
        followed = True
    return followed

  #共同的关注用户
  @property
  def common_id(self):
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
    return common_id

  @property
  def personal_info(self):
    personal_info = self.db.query('''SELECT gender,webchat_code,personal_profile 
                                  FROM user_info 
                                  WHERE user_uid=%s''',self.id)
    if personal_info:
      return personal_info
    else:
      return False