#ArticlesHandler
    author_id = self.id
    #登录用户信息
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None
    #作者信息
    author_info = self.db.query("SELECT pic,username FROM user WHERE uid=%s",author_id)
    author_pic = author_info[0]['pic']
    author_name = author_info[0]['username']
    #登录用户是否已经关注过该作者
    follower = False
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("SELECT id FROM relation WHERE from_user_id=%s AND to_user_id=%s AND type='2'",current_user_id,author_id)
      if len(id) == 0:
        follower = False
      else:
        follower = True
    #作者的关注用户数
    if self.redis.exists('following_count_' + author_id):
      following_count = self.redis.get('following_count_' + author_id)
    else:
      following_count = self.db.query('''SELECT count(to_user_id) count 
                                         FROM relation 
                                         WHERE from_user_id=%s''',author_id)[0]['count']
      self.redis.set('following_count_' + author_id,following_count)
    #作者的文章数
    if self.redis.exists('article_count_' + author_id):
      count_article = self.redis.get('article_count_' + author_id)
    else:
      count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",author_id)[0]['count']
      self.redis.set('article_count_' + author_id,count_article)
    #作者的粉丝数
    if self.redis.exists('follower_count_' + author_id):
      follower_count = self.redis.get('follower_count_' + author_id)
    else:
      follower_count = self.db.query('''SELECT count(from_user_id) count 
                                        FROM relation 
                                        WHERE to_user_id=%s''',author_id)[0]['count']
      self.redis.set('follower_count_' + author_id,follower_count)



#FollowingHandler

    author_id = self.id
    #登录用户信息
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None
    #作者信息
    author_info = self.db.query("SELECT pic,username FROM user WHERE uid=%s",author_id)
    author_pic = author_info[0]['pic']
    author_name = author_info[0]['username']
    #登录用户是否已经关注过该作者
    follower = False
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query('''SELECT id 
                            FROM relation 
                            WHERE from_user_id=%s 
                            AND to_user_id=%s 
                            AND type=\'2\'''',current_user_id,author_id)
      if len(id) == 0:
        follower = False
      else:
        follower = True
    #作者的关注数
    if self.redis.exists('following_count_' + author_id):
      following_count = self.redis.get('following_count_' + author_id)
    else:
      following_count = self.db.query("SELECT count(to_user_id) count FROM relation WHERE from_user_id=%s",author_id)[0]['count']
      self.redis.set('following_count_' + author_id,following_count)
    #作者的文章数
    if self.redis.exists('article_count_' + author_id):
      count_article = self.redis.get('article_count_' + author_id)
    else:
      count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",author_id)[0]['count']
      self.redis.set('article_count_' + author_id,count_article)
    #作者的粉丝数
    if self.redis.exists('follower_count_' + author_id):
      follower_count = self.redis.get('follower_count_' + author_id)
    else:
      follower_count = self.db.query("SELECT count(from_user_id) count FROM relation WHERE to_user_id=%s",author_id)[0]['count']
      self.redis.set('follower_count_' + author_id,follower_count)

##FollowersHandler
    author_id = self.id
    #登录用户信息
    if self.current_user:
      login_user_info = self.db.query("SELECT uid,pic FROM user WHERE username=%s",self.current_user)
      login_user_pic = login_user_info[0]['pic']
      login_user_id = login_user_info[0]['uid']
      login_user = self.current_user
    else:
      login_user_pic = None
      login_user_id = None
      login_user = None
    #作者信息
    author_info = self.db.query("SELECT pic,username FROM user WHERE uid=%s",author_id)
    author_pic = author_info[0]['pic']
    author_name = author_info[0]['username']
    #是否已经关注
    follower = False
    if self.current_user:
      current_user_id = self.db.query("SELECT uid FROM user WHERE username=%s",self.current_user)[0]['uid']
      id = self.db.query("select id from relation where from_user_id=%s and to_user_id=%s and type='2'",current_user_id,author_id)
      if len(id) == 0:
        follower = False
      else:
        follower = True
    #作者的关注数
    if self.redis.exists('following_count_' + author_id):
      following_count = self.redis.get('following_count_' + author_id)
    else:
      following_count = self.db.query("SELECT count(to_user_id) count FROM relation WHERE from_user_id=%s",author_id)[0]['count']
      self.redis.set('following_count_' + author_id,following_count)
    #作者的文章数
    if self.redis.exists('article_count_' + author_id):
      count_article = self.redis.get('article_count_' + author_id)
    else:
      count_article = self.db.query("SELECT COUNT(*) count FROM articles WHERE  user_uid=%s",author_id)[0]['count']
      self.redis.set('article_count_' + author_id,count_article)
    #作者的粉丝数
    if self.redis.exists('follower_count_' + author_id):
      follower_count = self.redis.get('follower_count_' + author_id)
    else:
      follower_count = self.db.query("SELECT count(from_user_id) count FROM relation WHERE to_user_id=%s",author_id)[0]['count']
      self.redis.set('follower_count_' + author_id,follower_count)