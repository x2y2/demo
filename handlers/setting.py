#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
from forms.form import BasicsettingForm
from forms.form import ChangepasswordForm
import os
import hashlib
import base64

class SettingHandler(BaseHandler):
  def get(self,*args,**kwargs):
    self.login_user_infos()
    self.personal_infos()

    action = "_%s_action" % self.arg
    if hasattr(self,action):
      getattr(self,action)(self.user_infos)


  def _basic_action(self,user_infos):
    self.render("setting.html",user_infos=user_infos)

  def _profile_action(self,user_infos):
    self.render("profile.html",user_infos=user_infos)
  
  def _account_manage_action(self,user_infos):
    self.render("account_manage.html",user_infos = user_infos)

  def post(self,*args,**kwargs):
    action = self.arg
    action = "_%s_action" % action
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
        img_name = str_md5[0:16]+'.jpg'
        filepath = os.path.join(upload_path,img_name)
        with open (filepath,'wb') as up:
          up.write(meta['body'])
        self.db.execute("UPDATE user SET pic=%s WHERE username=%s",img_name,self.current_user)
      self.redirect('/setting/basic')

  def _info_action(self):
    form = BasicsettingForm(self.request.arguments)
    username = form.nickname.data
    email = form.email.data
    user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
    cur_email = self.db.query("SELECT email FROM user WHERE username=%s",self.current_user)[0]['email']
    
    if form.validate():
      if username == self.current_user:
        if email == "" or email == cur_email:
          self.json('success','更新成功')
        else:
          if not self._checkaccount_action(email):
            self.json('emailexists','邮箱已注册')
          else:
            try:
              self.db.execute("UPDATE user SET email=%s WHERE uid=%s",email,user_id)
              self.json('success','更新成功')
            except Exception as e:
              self.write({'message':e})
      elif username is None:
        self.json('nouser','用户名不可为空')
      else:
        if not self._checkaccount_action(username):
          self.json('userexists','用户已注册')
        else:
          if email == '' or email == cur_email:
            try:
              self.db.execute("UPDATE user SET username=%s WHERE uid=%s",username,user_id)
              self.session['username'] = username
              self.session.save()
              self.json('success','更新成功')
            except Exception as e:
              self.write({'message':e})
          else:
            if not self._checkaccount_action(email):
              self.json('emailexists','邮箱已注册')
            else:
              try:
                self.db.execute("UPDATE user SET username=%s,email=%s WHERE uid=%s",username,email,user_id)
                self.session['username'] = username
                self.session.save()
                self.json('success','更新成功')
              except Exception as e:
                self.write({'message':e})
    else:
      if username is None or username == '':
        self.json('userkong','用户名不可为空')


  def _checkaccount_action(self,account):
    uid = self.db.query("SELECT uid FROM user WHERE (username=%s or email=%s)",account,account)
    if len(uid) == 0:
      return True
    else:
      return False

  def _account_action(self):
    form = ChangepasswordForm(self.request.arguments)
    password = form.password.data
    origin_password64 = base64.b64encode(password)
    new = form.new.data
    new_password64 = base64.b64encode(new)
    confirm = form.confirm.data
    cur_password = self.db.query("SELECT password FROM user WHERE username=%s",self.current_user)
    cur_password = cur_password[0]['password']

    if form.validate():
      if origin_password64 != cur_password:
        self.json('errpassword','密码错误')
      else:
        if new == password:
           self.json('samepassword','新密码和原始密码相同')
        else:
          if new != confirm:
            self.json('errconfirm','两次输入的密码不一致')
          else:
            try:
              self.db.execute("UPDATE user SET password=%s WHERE username=%s",new_password64,self.current_user)
              self.json('success','修改密码成功')
            except Exception as e:
              self.write({'message':e})
    else:
      if password is None or password == '' or new is None or new == '' or confirm is None or confirm == '':
        self.json('nopassword','密码不能为空')
      else:
        self.json('errconfirm','两次输入的密码不一致')
   
  def _webchat_upload_action(self):
    if self.request.files:
      upload_path = "/home/wangpei/demo/statics/upload/webchat/"
      file_metas = self.request.files['webchat-upload-pic']
      for meta in file_metas:
        filename = meta['filename']
        str = ''.join([self.current_user,filename])
        str_md5 = hashlib.md5(str).hexdigest()
        img_name = str_md5[0:16]+'.jpg'
        filepath = os.path.join(upload_path,img_name)
        with open (filepath,'wb') as up:
          up.write(meta['body'])
        if self._check_id():
          self.db.execute('''UPDATE user_info 
                             SET webchat_code=%s 
                             WHERE user_uid 
                             IN (SELECT uid 
                                  FROM user 
                                  WHERE username=%s)''',img_name,self.current_user)
        else:
          self.db.execute('''INSERT INTO user_info (user_uid,gender,personal_profile,webchat_code) 
                             VALUES ((SELECT uid 
                                      FROM user 
                                      WHERE username=%s),'','',%s)''',self.current_user,img_name)
      self.redirect('/setting/profile#')

  def _webchat_delete_action(self):
    login_user_id = self.get_argument('login_user_id',default="")
    try:
      self.db.execute('''UPDATE user_info SET webchat_code=%s WHERE user_uid=%s''','',login_user_id)
      self.json('success','ok')
    except Exception as e:
      self.json('error',e)

  def _personal_profile_action(self):
    login_user_id = self.get_argument('login_user_id',default="")
    gender_value = self.get_argument('gender',default="")
    if gender_value == 'male':
      gender = int(1)
    elif gender_value == 'female':
      gender = int(0)
    else:
      gender = int(2)
    personal_profile = self.get_argument('personal_profile',default="")
    try:
      if self._check_id():
        self.db.execute('''UPDATE user_info SET gender=%s,personal_profile=%s WHERE user_uid=%s''',gender,personal_profile,login_user_id)
      else:
        self.db.execute('''INSERT INTO user_info (user_uid,gender,personal_profile,webchat_code) 
                           VALUES (%s,%s,%s,'')''',login_user_id,gender,personal_profile)
      self.json('success','ok')
    except Exception as e:
      self.json('error',e)


  def _check_id(self):
    id = self.db.query('''SELECT id 
                          FROM user_info 
                          WHERE user_uid 
                          IN (SELECT uid 
                              FROM user 
                              WHERE username=%s)''',self.current_user)[0]['id']
    if id:
      return True
    else:
      return False




