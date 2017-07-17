#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
import os
import hashlib
import base64

class SettingHandler(BaseHandler):
  def get(self,*args,**kwargs):
    uri = self.request.uri
    page = uri.split('/')[-1]
    action = "_%s_action" % page
    if hasattr(self,action):
      getattr(self,action)()


  def _basic_action(self):
    pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
    pic_name = pic[0]['pic']
    self.render("setting.html",user=self.current_user,user_id=self.user_id,pic_name=pic_name)

  def _profile_action(self):
    pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
    pic_name = pic[0]['pic']
    self.render("profile.html",user=self.current_user,user_id=self.user_id,pic_name=pic_name)
  
  def _account_manage_action(self):
    pic = self.db.query("SELECT pic FROM user WHERE username=%s",self.current_user)
    pic_name = pic[0]['pic']
    self.render("account_manage.html",user=self.current_user,user_id=self.user_id,pic_name=pic_name)


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

  def _info_action(self):
    username = self.get_body_argument('setting-nickname',default="")
    email = self.get_body_argument('setting-email',default="")
    id = self.db.query("select id from user where username=%s",self.current_user)
    cur_email = self.db.query("select email from user where username=%s",self.current_user)
    cur_email = cur_email[0]['email']
    user_id = id[0]['id']

    if username == self.current_user:
      if email == "" or email == cur_email:
        self.redirect('/setting/basic')
      else:
        if not self._checkemail_action(email) or '@' not in email:
          self.redirect("/sign_up?error=exists&email={0}".format(email))
        else:
          self.db.execute("update user set email=%s where id=%s",email,user_id)
          self.redirect('/setting/basic')
    else:
      if not self._checkname_action(username) or username == "":
        self.redirect("/sign_up?error=exists&user={0}".format(username))
      else:
        if email == "" or email == cur_email:
          self.db.execute("update user set username=%s where id=%s",username,user_id)
          self.db.execute("update blogs set user_name=%s where user_id=%s",username,user_id)
          self.set_secure_cookie("username",username)
          self.redirect('/setting/basic') 
        else:
          if not self._checkemail_action(email):
            self.redirect("/sign_up?error=exists&email={0}".format(email))
          else:
            self.db.execute("update user set username=%s where id=%s",username,user_id)
            self.db.execute("update blogs set user_name=%s where user_id=%s",username,user_id)
            self.set_secure_cookie("username",username)
            self.db.execute("update user set email=%s where id=%s",email,user_id)
            self.redirect('/setting/basic')


  def _checkname_action(self,username):
    id = self.db.query("SELECT id FROM user WHERE username=%s",username)
    if len(id) == 0:
      return True
    else:
      return False

  def _checkemail_action(self,email):
    id = self.db.query("SELECT id FROM user WHERE email=%s",email)
    if len(id) == 0:
      return True
    else:
      return False   

  def _account_action(self):
    origin_password = self.get_body_argument('setting-origin-password',default="")
    origin_password64 = base64.b64encode(origin_password)
    new_password1 = self.get_body_argument('setting-new-password1',default="")
    new_password64 = base64.b64encode(new_password1)
    new_password2 = self.get_body_argument('setting-new-password2',default="")
    cur_password = self.db.query("select password from user where username=%s",self.current_user)
    cur_password = cur_password[0]['password']
    if origin_password == "" or new_password1 == "" or new_password2 == "":
      self.redirect("/setting/account_manage?error")
    else:
      if origin_password64 != cur_password:
        self.redirect("/setting/account_manage?password=wrong")
      else:
        if new_password1 == origin_password:
           self.redirect("/setting/account_manage?newpassword=originapassword")
        else:
          if new_password1 != new_password2:
            self.redirect("/setting/account_manage?newpassword=notright")
          else:
            self.db.execute("update user set password=%s where username=%s",new_password64,self.current_user)
            self.redirect("/setting/account_manage")
   