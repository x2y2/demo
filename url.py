#!/usr/bin/env python
#coding=utf8

from handlers.index import IndexHandler
from handlers.sign_up import SignUpHandler
from handlers.login import LoginHandler
from handlers.logout import LogoutHandler
from handlers.blog import BlogContentHandler
from handlers.blog import NewBlogHandler
from handlers.blog import EditBlogHandler
from handlers.blog import CommentBlogHandler
from handlers.users import UsersHandler
from handlers.users import FollowHandler
from handlers.users import FollowersHandler
from handlers.setting import SettingHandler
from handlers.contactus import ContactusHandler

url = [(r'/',IndexHandler)]
url += [(r'/index',IndexHandler)]
url += [(r'/sign_up',SignUpHandler)]
url += [(r'/login',LoginHandler)]
url += [(r'/logout',LogoutHandler)]
url += [(r'/blog/[0-9a-z]+',BlogContentHandler)]
url += [(r'/blog/new/(\w+)',NewBlogHandler)]
url += [(r'/blog/edit/(\w+)',EditBlogHandler)]
url += [(r'/blog/[0-9a-z]+/comment',CommentBlogHandler)]
url += [(r'/users/[0-9a-z]{16}',UsersHandler)]
url += [(r'/users/[0-9a-z]{16}/following[a-z_]{0,}',FollowHandler)]
url += [(r'/users/[0-9a-z]{16}/following',FollowHandler)]
url += [(r'/users/[0-9a-z]{16}/followers',FollowersHandler)]
url += [(r'/users/[0-9a-z]{16}/follower[a-z_]{0,}',FollowersHandler)]
url += [(r'/setting/\w+',SettingHandler)]
url += [(r'/setting/basic/\w+',SettingHandler)]
url += [(r'/setting/accouont?\w+',SettingHandler)]
url += [(r'/contactus',ContactusHandler)]

