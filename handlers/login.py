#!/usr/bin/env python
#coding=utf-8

import tornado.escape
import tornado.web
from base import BaseHandler
from wtforms.fields.core import UnboundField
from forms.form import LoginForm
import base64
import re

    
class LoginHandler(BaseHandler,LoginForm):
  '''
  def __getattribute__(self,item):
    ret = object.__getattribute__(self,item)
    if isinstance(ret,UnboundField):
      obj = object.__getattribute__(self,'form')
      return getattr(obj,item).data
    return ret
  '''
  def get(self):
    self.render("login.html")


  def post(self):
    #self.form = LoginForm(self)
    #account = self.account
    #password = self.password
    form = LoginForm(self.request.arguments)
    account = form.account.data
    password = form.password.data
    if password:
      password = base64.b64encode(password)
    cbox_remember = form.remeberme.data
    if form.validate():
      if '@' in account:
        email = account
        if not self._checkemail_action(email):
          self.json('noexists','用户不存在')
        else:
          if not self._checkpasswd_action(email,password):
            self.json('errorpassword','密码错误')
          else:
            ret = self.db.query("SELECT username FROM user WHERE email=%s",email)
            username = ret[0]['username']
            if cbox_remember:
              self.session['username'] = username
              self.session['timeout'] = 2592000
              self.session.save()
            else:
              self.session['username'] = username
              self.session['timeout'] = 60
              self.session.save()
            self.redirect('/')
      else:
        username = account
        if not self._checkname_action(username):
          self.json('noexists','用户不存在')
        else:
          if not self._checkpasswd_action(username,password):
            self.json('errorpassword','密码错误')
          else:
            if cbox_remember:
              #self.set_secure_cookie("username",username,xpires_days=30)
              self.session['username'] = username
              self.session['timeout'] = 2592000
              self.session.save()
            else:
              self.session['username'] = username
              self.session['timeout'] = 3600
              self.session.save()
            self.json('success','/')
    else:
      if not account:
        self.json('nouser','用户名不能为空')
      elif not password:
        self.json('nopassword','密码不能为空')
     
  def _checkemail_action(self,email):
    id = self.db.query("SELECT id FROM user WHERE email=%s",email)
    if len(id) == 0:
      return False
    else:
      return True

  def _checkname_action(self,username):
    id = self.db.query("SELECT id FROM user WHERE username=%s",username)
    if len(id) == 0:
      return False
    else:
      return True

  def _checkpasswd_action(self,account,password):
    if '@' in account:
      id = self.db.query("SELECT id FROM user WHERE (email=%s and password=%s)",account,password)
    else:
      id = self.db.query("SELECT id FROM user WHERE (username=%s and password=%s)",account,password)
    if not id:
      return False
    else:
      return True

  def _has_cn(self,text):
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    return zhPattern.search(text)
      


  