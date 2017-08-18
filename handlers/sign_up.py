#!/usr/bin/env python
#coding=utf-8

import tornado.web
import hashlib
from base import BaseHandler
from wtforms.fields.core import UnboundField
from wtforms.validators import ValidationError
from forms.form import SignupForm
import datetime
import base64

    
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
    #self.form = SignupForm(self)
    form = SignupForm(self.request.arguments)
    if form.validate():
      email = form.data['email']
      username = form.data['username']
      password = form.data['password']
      password = base64.b64encode(password)
      register_time = datetime.datetime.now().strftime('%Y-%m-%d\ %H:%M:%S')
      md5 = hashlib.md5(username).hexdigest()
      uid = md5[0:16]
      if not self._checkusername_action(username,email):
        self.db.execute('''INSERT INTO user 
                          (uid,username,password,email,register_time,admin)
                           VALUES
                           (%s,%s,%s,%s,%s,'0')''',
                           uid,username,password,email,register_time)
        self.redirect("/login")
      else:
        self.redirect("/sign_up?error=exists&user={0}&email={1}".format(username,email))
    else:
      self.redirect("/sign_up")

  def _checkusername_action(self,username,email):
    user_id = self.db.query("SELECT id FROM user WHERE (username=%s OR email=%s)",username,email)
    if len(user_id) == 0:
      return False
    else:
      return True