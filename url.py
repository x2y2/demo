#!/usr/bin/env python
#coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from handlers.index import IndexHandler
from handlers.login import LoginHandler
from handlers.logout import LogoutHandler
from handlers.blog import BlogContentHandler

url = [(r'/',IndexHandler),
       (r'/index',IndexHandler),
       (r'/index/[a-zA-Z0-9]+',IndexHandler),
       (r'/login',LoginHandler),
       (r'/logout',LogoutHandler),
       (r'/blog/[0-9]+',BlogContentHandler)
      ]
