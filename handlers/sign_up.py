#!/usr/bin/env python
#coding=utf-8

import tornado.web
import hashlib
from base import BaseHandler
from wtforms.fields.core import UnboundField
from wtforms import ValidationError
from forms.form import SignupForm
import datetime
import base64
import json

    
class SignUpHandler(BaseHandler,SignupForm):
  '''
  def __getattribute__(self,item):
    ret = object.__getattribute__(self,item)
    if isinstance(ret,UnboundField):
      obj = object.__getattribute__(self,'form')
      return getattr(obj,item).data
    return ret
  '''

  def get(self):
    self.render("sign_up.html")

  def post(self):
    form = SignupForm(self.request.arguments)
    email = form.email.data
    username = form.username.data
    password = form.password.data
    if form.validate():
      password = base64.b64encode(password)
      register_time = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
      md5 = hashlib.md5(username).hexdigest()
      uid = md5[0:16]
      if self._checkaccount_action(username):
        self.json('userexists','用户已注册')
      elif self._checkaccount_action(email):
        self.json('emailexists','邮箱已注册')
      else:
        try:
          self.db.execute('''INSERT INTO user 
                             (uid,username,password,email,register_time,admin)
                             VALUES(%s,%s,%s,%s,%s,'0')''',
                             uid,username,password,email,register_time)
          self.json('success','/login')
        except Exception as e:
          self.write({'message':json.dumps(e)})
    else:
      if not username:
        self.json('nouser','用户名不能为空')
      elif not email:
        self.json('noemail','邮箱不能为空')
      elif not password:
        self.json('nopassword','密码不能为空')
      else:
        self.json('emailformat','邮箱格式不对')

  def _checkaccount_action(self,account):
    user_id = self.db.query("SELECT id FROM user WHERE (username=%s or email=%s)",account,account)
    if len(user_id) == 0:
      return False
    else:
      return True