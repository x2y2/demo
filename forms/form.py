#!/usr/bin/env python
#coding:utf-8
import wtforms
from wtforms import validators,fields
from wtforms_tornado import Form 
from wtforms.fields.core import UnboundField
from wtforms import ValidationError

class MultiDict(dict):
  def getlist(self,key):
    return self[key]

  def setlist(self,key,value):
    self[key] = value

class BaseForm(Form):
  def __init__(self,handler=None,obj=None,prefix='',**kwargs):
    if handler is None:
      return
    formdata = MultiDict()
    if handler.request.method == 'POST':
      for name in handler.request.arguments.keys():
        formdata.setlist(name,handler.get_arguments(name))
    else:
      for name in handler.request.query_arguments.keys():
        formdata.setlist(name,handler.request.query_arguments[name])
    Form.__init__(self,formdata,obj=obj,prefix=prefix,**kwargs)
 
 #class LoginForm(BaseForm):
    pass

   
class LoginForm(Form):
  account = fields.StringField(validators=[validators.required()])
  password = fields.PasswordField(validators=[validators.required()])
  remeberme = fields.BooleanField(validators=[validators.required()])

class SignupForm(Form):
  email = fields.StringField(validators=[validators.Email(),validators.required(), validators.length(max=64)])
  username = fields.StringField(validators=[validators.required(),validators.length(max=10)])
  password = fields.PasswordField(validators=[validators.required()])

class BasicsettingForm(Form):
  nickname = fields.StringField(validators=[validators.required(),validators.length(max=10)])
  email = fields.StringField(validators=[validators.length(max=64)])
    
class ChangepasswordForm(Form):
  password = fields.PasswordField(validators=[validators.required()])
  new = fields.PasswordField(validators=[validators.required(),validators.EqualTo('confirm')])
  confirm = fields.PasswordField(validators=[validators.required()])
