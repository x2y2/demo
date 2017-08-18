#!/usr/bin/env python
#coding=utf-8

from base import BaseHandler
from forms.form import BasicsettingForm
import os
import hashlib
import base64

class SettingHandler(BaseHandler):
  def get(self,*args,**kwargs):
    #登录用户信息
    if self.current_user is not None:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None

    action = "_%s_action" % self.arg
    if hasattr(self,action):
      getattr(self,action)(login_user,login_user_id,login_user_pic)


  def _basic_action(self,login_user,login_user_id,login_user_pic):
    self.render("setting.html",
                 login_user=login_user,
                 login_user_id=login_user_id,
                 login_user_pic=login_user_pic)

  def _profile_action(self,login_user,login_user_id,login_user_pic):
    if self.personal_info:
      gender = self.personal_info[0]['gender']
      webchat_code = self.personal_info[0]['webchat_code']
      personal_profile = self.personal_info[0]['personal_profile']
    else:
      gender = webchat_code = personal_profile =None
    self.render("profile.html",
                 login_user=login_user,
                 login_user_id=login_user_id,
                 login_user_pic=login_user_pic,
                 gender =  gender,
                 webchat_code=webchat_code,
                 personal_profile=personal_profile)
  
  def _account_manage_action(self,login_user,login_user_id,login_user_pic):
    self.render("account_manage.html",
                 login_user=login_user,
                 login_user_id=login_user_id,
                 login_user_pic=login_user_pic)

  def post(self,*args,**kwargs):
    self.form = BasicsettingForm(self.request.arguments)
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
    #username = self.get_body_argument('nickname',default="")
    #email = self.get_body_argument('email',default="")
    username = self.form.data['nickname']
    email = self.form.data['email']
    uid = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)
    user_id = uid[0]['uid']
    cur_email = self.db.query("SELECT email FROM user WHERE username=%s",self.current_user)
    cur_email = cur_email[0]['email']
    
    #if self.form.validate():
    if username == self.current_user:
      if email == "" or email == cur_email:
        self.redirect('/setting/basic')
      else:
        if not self._checkemail_action(email) or '@' not in email:
          self.redirect("/sign_up?error=exists&email={0}".format(email))
        else:
          self.db.execute("UPDATE user SET email=%s WHERE uid=%s",email,user_id)
          self.redirect('/setting/basic')
    else:
      if not self._checkname_action(username) or username == "":
        self.redirect("/sign_up?error=exists&user={0}".format(username))
      else:
        if email == "" or email == cur_email:
          self.db.execute("UPDATE user SET username=%s WHERE uid=%s",username,user_id)
          #self.set_secure_cookie("username",username)
          self.session['username'] = username
          self.session.save()
          self.redirect('/setting/basic') 
        else:
          if not self._checkemail_action(email):
            self.redirect("/sign_up?error=exists&email={0}".format(email))
          else:
            self.db.execute("UPDATE user SET username=%s WHERE uid=%s",username,user_id)
            #self.set_secure_cookie("username",username)
            self.session['username'] = username
            self.session.save()
            self.db.execute("UPDATE user SET email=%s WHERE uid=%s",email,user_id)
            self.redirect('/setting/basic')
    #else:
    #  self.redirect('/setting/basic')


  def _checkname_action(self,username):
    uid = self.db.query("SELECT uid FROM user WHERE username=%s",username)
    if len(uid) == 0:
      return True
    else:
      return False

  def _checkemail_action(self,email):
    uid = self.db.query("SELECT uid FROM user WHERE email=%s",email)
    if len(uid) == 0:
      return True
    else:
      return False   

  def _account_action(self):
    origin_password = self.get_body_argument('setting-origin-password',default="")
    origin_password64 = base64.b64encode(origin_password)
    new_password1 = self.get_body_argument('setting-new-password1',default="")
    new_password64 = base64.b64encode(new_password1)
    new_password2 = self.get_body_argument('setting-new-password2',default="")
    cur_password = self.db.query("SELECT password FROM user WHERE username=%s",self.current_user)
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
            self.db.execute("UPDATE user SET password=%s WHERE username=%s",new_password64,self.current_user)
            self.redirect("/setting/account_manage")
   
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




