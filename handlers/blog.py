#!/usr/bin/env python
#coding=utf8

from base import BaseHandler
from user_main import UserBaseHandler as UBH
import sys
import datetime
import hashlib
import markdown2
import HTMLParser
import json
import ujson


reload(sys)
sys.setdefaultencoding('utf8')

class BlogContentHandler(UBH):
  def get(self):
    #登录用户信息
    UBH.login_user_infos(self)
    bid = self.id
    #记录阅读次数
    self.db.execute("update articles set read_count=read_count + 1 where aid=%s",bid)
    #文章信息
    b_infos = self.db.query('''SELECT 
                                  u.uid,
                                  u.username,
                                  u.pic,
                                  a.aid,
                                  a.title,
                                  a.content,
                                  a.created_at,
                                  a.comment_count,
                                  a.read_count 
                                FROM articles a,user u 
                                WHERE 
                                  a.user_uid=u.uid 
                                AND 
                                  a.aid=%s
                            ''',bid
                            )
    c_infos = b_infos[0]['content']
    html = markdown2.markdown(c_infos)
    #html_parser = HTMLParser.HTMLParser()
    #html = html_parser.unescape(c_infos_html)
    #评论信息
    comment_infos = self.db.query('''SELECT u.uid,u.username,u.pic,c.comment_cid,c.comment_time,c.comment_content,c.comment_floor 
                                     FROM comments c,user u 
                                     WHERE c.user_uid=u.uid 
                                     AND c.article_aid=%s 
                                     ORDER BY comment_time 
                                     DESC''',bid)
    #是否已对评论点赞
    upvote_state = {}
    for comment_info in comment_infos:
      upvote_state[comment_info['comment_cid']] = 0

    try:
      upvote_infos = self.db.query('''SELECT comment_cid,state 
                                      FROM upvote 
                                      WHERE article_aid=%s AND user_uid IN 
                                            (SELECT uid FROM user WHERE username=%s)''',
                                            bid,self.current_user)
      for upvote_info in upvote_infos:
        upvote_state[upvote_info['comment_cid']] = upvote_info['state']
    except Exception as e:
      self.write({'message':e})
    #文章对应评论的点赞数
    upvote_counts = self.db.query('''SELECT c.article_aid,c.comment_cid,up.upid,up.state
                                    FROM comments  c left join upvote up on c.comment_cid=up.comment_cid 
                                    WHERE c.article_aid=%s''',bid)
    dic_upvote = {}
    for upvote_count in upvote_counts:
      dic_upvote[upvote_count['comment_cid']] = 0

    for upvote_count in upvote_counts:
      if upvote_count['state'] == '1':
        dic_upvote[upvote_count['comment_cid']] += 1

    #是否已经关注过
    author_id = b_infos[0]['uid']
    followed = False
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("SELECT id FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,author_id)
      if len(id) == 0:
        followed = False
      else:
        followed = True

    self.render("blog.html",
                b_infos=b_infos,
                c_infos_html= html,
                user_infos = UBH.user_infos,
                comment_infos=comment_infos,
                followed=followed,
                upvote_state=upvote_state,
                dic_upvote=dic_upvote)

  def post(self,*args,**kwargs):
    author_id = self.get_argument("author_id",default="")
    current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    url = self.get_argument("url",default="")
    string = url.split('/')[-1]
    action = "_%s_action" % string
    if self.current_user:
      if hasattr(self,action):
        getattr(self,action)(author_id,current_user_id)
    else:
      self.redirect('/login')


  def _following_add_action(self,author_id,current_user_id):
    try:
      self.db.execute('''INSERT INTO relation(from_user_id,to_user_id,type) VALUES(%s,%s,'2')''',current_user_id,author_id)
      self.redis.incr('following_count_' + current_user_id)
      self.redis.incr('follower_count_' + author_id)
      self.json('success','/blog/' + self.id)
    except Exception as e:
      self.write(json.dumps({'error',e}))

  #取消关注作者
  def _following_remove_action(self,author_id,current_user_id):
    try:
      self.db.execute("DELETE FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,author_id)
      self.redis.decr('following_count_'+ current_user_id)
      self.redis.decr('follower_count_'+ author_id)
      self.json('success','/blog/' + self.id)
    except Exception as e:
      self.json('error',e)

class NewBlogHandler(UBH):
  def get(self,*args,**kwargs):
    UBH.login_user_infos(self)
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)(UBH.user_infos)
    else:
      m_infos = self.db.query("select id,title from articles")
      self.render("index.html",m_infos = m_infos,user_infos=UBH.user_infos)

  def _info_action(self,user_infos):
    self.render("newblog.html",user_infos=user_infos)

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
    user_id = self.db.query("SELECT uid FROM user WHERE username=%s",user_name)[0]['uid']
    created_at = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
    str = ''.join([created_at,user_name])
    str_md5 = hashlib.md5(str).hexdigest()
    blog_id = str_md5[0:16]
    try:
      self.db.execute('''INSERT INTO articles
                          (aid,
                           user_uid,
                           title,
                           content,
                           created_at
                           )
                           VALUES
                           (%s,%s,%s,%s,%s
                           )''',
                           blog_id,
                           user_id,
                           blog_title,
                           blog_content,
                           created_at)
      self.redis.incr('article_count_' + user_id)
      self.json("success",blog_id)
    except Exception as e:
      self.json('error',str(e))

class EditBlogHandler(UBH):
  def get(self,*args,**kwargs):
    UBH.login_user_infos(self)
    action = "_%s_action" % args[0]
    if hasattr(self,action):
      getattr(self,action)(UBH.user_infos)
    else:
      m_infos = self.db.query("select aid,title from articles")
      self.render("index.html",
                   m_infos = m_infos,
                   user_infos = UBH.user_infos)

  def _info_action(self,user_infos):
    blog_id = self.get_argument('id',default="")
    blog_title_content = self.db.query("select title,content from articles where aid=%s",blog_id)
    self.render("editblog.html",
                 user_infos = user_infos,
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
    blog_title = self.get_argument("blog_title",default="")
    blog_content = self.get_argument("blog_content",default="")
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
      self.redis.decr('article_count_' + uid)
      self.json("success",uid)
    except Exception as e:
      self.json("error",str(e))


class CommentBlogHandler(BaseHandler):
  def post(self,*args,**kwargs):
    action = "_%s_action" % self.arg
    if hasattr(self,action):
      getattr(self,action)()
    else:
      self.json("fail","no action")

  def _add_comment_action(self):
    article_aid = self.get_body_argument('article_aid',default='')
    comment_content = self.get_body_argument('new-comment',default='')
    comment_user = self.current_user
    comment_time = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
    str = ''.join([comment_time,comment_user])
    str_md5 = hashlib.md5(str).hexdigest()
    comment_cid = str_md5[0:16]
    #评论楼层
    max_f = self.db.query("select max(comment_floor) max_f from comments where article_aid=%s",article_aid)[0]['max_f']
    if not max_f:
      max_f = 0
    comment_floor = int(max_f) + 1
    
    if comment_content:
      try:
        self.db.execute('''INSERT INTO comments(
                                        user_uid,
                                        article_aid,
                                        comment_cid,
                                        comment_content,
                                        comment_time,
                                        comment_floor,
                                        comment_flag
                                                )
                           VALUES
                                  ((select uid from user where username=%s),
                                   %s,%s,%s,%s,%s,'0')''',
                                   comment_user,
                                   article_aid,
                                   comment_cid,
                                   comment_content,
                                   comment_time,
                                   comment_floor
                                   )
        comment_count = self.db.query("select comment_count from articles where aid=%s",article_aid)[0]['comment_count']
        if not comment_count:
          comment_count = 0
        comment_count = int(comment_count) + 1
        self.db.execute("update articles set comment_count=%s where aid=%s",comment_count,article_aid)
        self.redirect("/blog/" + article_aid)
      except Exception as e:
        pass
        #self.write(json.dumps({'messsage':e}))
    else:
      self.redirect("/blog/" + article_aid)

  def _add_upvote_action(self):
    user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    article_aid = self.get_argument('blog_id',default='')
    comment_cid = self.get_argument('comment_id',default='')
    #生成upvote_id值
    upvote_user = self.current_user
    upvote_time = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
    str = ''.join([upvote_time,upvote_user])
    str_md5 = hashlib.md5(str).hexdigest()
    upid = str_md5[0:16]
    if self._check_upvote(user_id,article_aid,comment_cid) == False:
      try:
        self.db.execute('''INSERT INTO upvote (upid,article_aid,user_uid,comment_cid,state) 
                           VALUES (%s,%s,%s,%s,'1')''',upid,article_aid,user_id,comment_cid)
        self.json('success',upid)
      except Exception as e:
        self.write({'message':e})
    elif self._check_upvote(user_id,article_aid,comment_cid) == '1':
      try:
        self.db.execute('''UPDATE upvote SET state='0' WHERE user_uid=%s AND article_aid=%s AND comment_cid=%s''',
                           user_id,article_aid,comment_cid)
        self.json('success',upid)
      except Exception as e:
        self.write({'message':e})
    else:
      try:
        self.db.execute('''UPDATE upvote SET state='1' WHERE user_uid=%s AND article_aid=%s AND comment_cid=%s''',
                           user_id,article_aid,comment_cid)
        self.json('success',upid)
      except Exception as e:
        self.write({'message':e})

  def _check_upvote(self,user_id,article_aid,comment_cid):
    info = self.db.query('''SELECT id,state 
                          FROM upvote 
                          WHERE user_uid=%s AND article_aid=%s AND comment_cid=%s''',
                          user_id,article_aid,comment_cid)
    if len(info) != 0:
      if info[0]['state'] == '1':
        return '1'
      else:
        return '0'
    else:
      return False
    