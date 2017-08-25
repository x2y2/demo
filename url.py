#!/home/wangpei/venv/bin/python
#coding=utf8

from handlers.index import IndexHandler
from handlers.sign_up import SignUpHandler
from handlers.login import LoginHandler
from handlers.logout import LogoutHandler
from handlers.blog import BlogContentHandler
from handlers.blog import NewBlogHandler
from handlers.blog import EditBlogHandler
from handlers.blog import CommentBlogHandler
from handlers.users import ArticlesHandler
from handlers.users import FollowingHandler
from handlers.users import FollowersHandler
from handlers.setting import SettingHandler
from handlers.contactus import ContactusHandler

url = [(r'/',IndexHandler)]
url += [(r'/index',IndexHandler)]
url += [(r'/sign_up',SignUpHandler)]
url += [(r'/login',LoginHandler)]
url += [(r'/logout',LogoutHandler)]
url += [(r'/blog/[0-9a-z]{16}',BlogContentHandler)]
url += [(r'/blog/[0-9a-z]{16}/following_add',BlogContentHandler)]
url += [(r'/blog/[0-9a-z]{16}/following_remove',BlogContentHandler)]
url += [(r'/blog/new/(\w+)',NewBlogHandler)]
url += [(r'/blog/edit/(\w+)',EditBlogHandler)]
url += [(r'/blog/[0-9a-z]{16}/[a-z_]+',CommentBlogHandler)]
url += [(r'/users/[0-9a-z]{16}',ArticlesHandler)]
url += [(r'/users/[0-9a-z]{16}/personal_profile_save',ArticlesHandler)]
url += [(r'/users/[0-9a-z]{16}/following[a-z_]{0,}',FollowingHandler)]
url += [(r'/users/[0-9a-z]{16}/following',FollowingHandler)]
url += [(r'/users/[0-9a-z]{16}/followers',FollowersHandler)]
url += [(r'/users/[0-9a-z]{16}/follower[a-z_]{0,}',FollowersHandler)]
url += [(r'/setting/\w+',SettingHandler)]
url += [(r'/setting/basic/\w+',SettingHandler)]
url += [(r'/setting/profile/\w+',SettingHandler)]
url += [(r'/setting/account?\w+',SettingHandler)]
url += [(r'/contactus',ContactusHandler)]

