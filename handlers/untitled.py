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


#session

import uuid   
import hmac   
import ujson   
import hashlib   
import redis   
class SessionData(dict):   
    def __init__(self, session_id, hmac_key):   
        self.session_id = session_id   
        self.hmac_key = hmac_key   
  
class Session(SessionData):   
    def __init__(self, session_manager, request_handler):   
        self.session_manager = session_manager   
        self.request_handler = request_handler   
        try:   
            current_session = session_manager.get(request_handler)   
        except InvalidSessionException:   
            current_session = session_manager.get()   
        for key, data in current_session.iteritems():   
            self[key] = data   
        self.session_id = current_session.session_id   
        self.hmac_key = current_session.hmac_key
 
    def save(self):   
        self.session_manager.set(self.request_handler, self)   
class SessionManager(object):   
    def __init__(self, secret, store_options, session_timeout):   
        self.secret = secret   
        self.session_timeout = session_timeout   
        try:   
            if store_options['redis_pass']:   
                self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'], password=store_options['redis_pass'])   
            else:   
                self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'])   
        except Exception as e:   
            print e
 
    def _fetch(self, session_id):   
        try:   
            session_data = raw_data = self.redis.get(session_id)   
            if raw_data != None:   
                self.redis.setex(session_id, self.session_timeout, raw_data)   
                session_data = ujson.loads(raw_data)   
            if type(session_data) == type({}):   
                return session_data   
            else:   
                return {}   
        except IOError:   
            return {}   
    def get(self, request_handler = None):   
        if (request_handler == None):   
            session_id = None   
            hmac_key = None   
        else:   
            session_id = request_handler.get_secure_cookie("session_id")   
            hmac_key = request_handler.get_secure_cookie("verification")   
        if session_id == None:   
            session_exists = False   
            session_id = self._generate_id()   
            hmac_key = self._generate_hmac(session_id)   
        else:   
            session_exists = True   
        check_hmac = self._generate_hmac(session_id)   
        if hmac_key != check_hmac:   
            raise InvalidSessionException()   
        session = SessionData(session_id, hmac_key)   
        if session_exists:   
            session_data = self._fetch(session_id)   
            for key, data in session_data.iteritems():   
                session[key] = data   
        return session 
 
    def set(self, request_handler, session):   
        request_handler.set_secure_cookie("session_id", session.session_id)   
        request_handler.set_secure_cookie("verification", session.hmac_key)   
        session_data = ujson.dumps(dict(session.items()))   
        self.redis.setex(session.session_id, self.session_timeout, session_data)   
    def _generate_id(self):   
        new_id = hashlib.sha256(self.secret + str(uuid.uuid4()))   
        return new_id.hexdigest()   
    def _generate_hmac(self, session_id):   
        return hmac.new(session_id, self.secret, hashlib.sha256).hexdigest()   
class InvalidSessionException(Exception):   
    pass 