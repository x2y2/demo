#!/usr/bin/env python
import wtforms
from wtforms import validators,fields
from wtforms_tornado import Form 
from wtforms.fields.core import UnboundField

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
 # email = fields.StringField(validators=[validators.Email(), validators.required(), validators.length(min=5, max=64)])
 # account = fields.StringField(validators=[validators.required(),validators.length(min=3,max=10)])
 # password = fields.PasswordField(validators=[validators.required()])

   
class LoginForm(Form):
  email = fields.StringField(validators=[validators.Email(), validators.required(), validators.length(min=5, max=64)])
  account = fields.StringField(validators=[validators.required(),validators.length(min=3,max=10)])
  password = fields.PasswordField(validators=[validators.required()])

class SignupForm(Form):
  email = fields.StringField(validators=[validators.Email(), validators.required(), validators.length(min=5, max=64)])
  username = fields.StringField(validators=[validators.required(),validators.length(min=3,max=10)])
  password = fields.PasswordField(validators=[validators.required()])

class BasicsettingForm(Form):
  nickname = fields.StringField(validators=[validators.required(),validators.length(min=3,max=10)])
  email = fields.StringField(validators=[validators.Email(), validators.length(min=5, max=64)])
    