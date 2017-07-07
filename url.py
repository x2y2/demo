#!/usr/bin/env python
#coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from handlers.index import IndexHandler
from handlers.sign_up import SignUpHandler
from handlers.login import LoginHandler
from handlers.logout import LogoutHandler
from handlers.blog import BlogContentHandler
from handlers.blog import NewBlogHandler
from handlers.blog import EditBlogHandler
from handlers.blog import UploadHandler



url = [(r'/',IndexHandler)]
url += [(r'/index',IndexHandler)]
url += [(r'/index/[a-zA-Z0-9]+',IndexHandler)]
url += [(r'/sign_up',SignUpHandler)]
url += [(r'/login',LoginHandler)]
url += [(r'/logout',LogoutHandler)]
url += [(r'/blog/[a-zA-Z0-9_=]+',BlogContentHandler)]
url += [(r'/blog/new/(\w+)',NewBlogHandler)]
url += [(r'/blog/edit/(\w+)',EditBlogHandler)]
url += [(r'/blog/upload/(\w+)',UploadHandler)]

