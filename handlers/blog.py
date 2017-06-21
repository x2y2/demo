#!/usr/bin/env python
#coding=utf8

import tornado.web
from base import BaseHandler
import methods.db as db
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class BlogContentHandler(BaseHandler):
  def get(self):
    uri = self.request.uri
    page = int(uri.split('/')[-1])
    b_infos = db.select_blog_content(table='blogs',column='*')
    b_infos = b_infos
    self.render("blog.html",b_infos=b_infos,user=self.current_user,page=page)