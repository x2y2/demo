#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
import hashlib


class UsersHandler(BaseHandler):
  def get(self):
    self.render("users.html",user=self.current_user,user_id=self.user_id)

class UserArticleHandler(BaseHandler):  
  def get(self):
    query = self.get_argument("order_by",default="")
    action = "_%s" % query
    if hasattr(self,action):
      getattr(self,action)()


  def _created_at(self):
    read = 0
    comment = 0
    good = 0
    count_article = self.db.query('''SELECT 
                                        COUNT(*) count
                                     FROM blogs 
                                     WHERE user_id=
                                          (SELECT 
                                              id 
                                           FROM
                                              user 
                                           WHERE 
                                              username=%s
                                          )''',self.current_user
                                  )

    m_infos = self.db.query('''SELECT 
                                 id,
                                 user_name,
                                 title,
                                 content,
                                 created_at 
                               FROM
                                 blogs 
                               WHERE 
                                 user_id=(
                                 SELECT 
                                  id 
                                 FROM 
                                  user 
                                 WHERE 
                                  username=%s)
                               ORDER BY 
                                 created_at DESC''',self.current_user)
    self.render("users.html",
                user=self.current_user,
                user_id=self.user_id,
                m_infos=m_infos,
                count_article=count_article,
                read=read,
                comment=comment,
                good=good
                )


