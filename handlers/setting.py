#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
import os
import hashlib

class SettingHandler(BaseHandler):
  def get(self,*args):
    pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
    pic_name = pic[0]['pic']
    self.render("setting.html",user=self.current_user,user_id=self.user_id,pic_name=pic_name)

  def post(self,*args,**kwargs):
    uri = self.request.uri
    page = uri.split('/')[-1]
    action = "_%s_action" % page
    if hasattr(self,action):
      getattr(self,action)()
    else:
      self.json("fail","no action")

  def _upload_action(self):
    if self.request.files:
      upload_path = "/home/wangpei/demo/statics/upload/img"
      file_metas = self.request.files['upload-pic']
      for meta in file_metas:
        filename = meta['filename']
        str = ''.join([self.current_user,filename])
        str_md5 = hashlib.md5(str).hexdigest()
        img_name = str_md5[0:16]
        filepath = os.path.join(upload_path,img_name)
        with open (filepath,'wb') as up:
          up.write(meta['body'])
        self.db.execute("UPDATE user SET pic=%s WHERE username=%s",img_name,self.current_user)
      self.redirect('/setting/basic')
  