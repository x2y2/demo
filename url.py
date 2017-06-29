#!/usr/bin/env python
#coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from handlers.index import IndexHandler
from handlers.login import LoginHandler
from handlers.logout import LogoutHandler
from handlers.blog import BlogContentHandler
from handlers.blog import NewBlogHandler

url = [(r'/',IndexHandler)]
url += [(r'/index',IndexHandler)]
url += [(r'/index/[a-zA-Z0-9]+',IndexHandler)]
url += [(r'/login',LoginHandler)]
url += [(r'/logout',LogoutHandler)]
url += [(r'/blog/[0-9]+',BlogContentHandler)]
url += [(r'/blog/new/(\w+)',NewBlogHandler)]
