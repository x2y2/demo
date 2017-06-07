#!/usr/bin/env python
#coding=utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from handlers.index import IndexHandler
from handlers.user import UserHandler

url = [(r'/',IndexHandler),
       (r'/user',UserHandler),
      ]
