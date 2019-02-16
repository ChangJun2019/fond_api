# -*- coding: utf-8 -*-
# @Time     : 2018/8/21 23:08
# @Author   : ChangJun
# @Email    : 52chinaweb@gmail.com
# @Function : 用户数据模型

from sqlalchemy import Column, Integer, String, SmallInteger, Text
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import AuthFailed, NotFound, ParameterException
from app.models.base import Base, db


class User(Base):
    """ 用户数据模型 """
    id = Column(Integer, primary_key=True)
    account = Column(String(24), unique=True)
    nickname = Column(String(24), unique=True)
    avatar = Column(String(255))
    city = Column(String(24))
    gender = Column(String(10))
    openid = Column(String(50), unique=True)  # 微信身份标识
    mobile = Column(String(25))
    province = Column(String(10))
    auth = Column(SmallInteger, default=1)
    pro = Column(String(50))  # 职业
    tags = Column(Text)  # 标签
    email = Column(String(150), unique=True)  # 邮箱
    country = Column(String(15))
    sig = Column(String(100))  # 个签
    _password = Column('password', String(100))

    def keys(self):
        return ['id', 'nickname', 'avatar', 'gender', 'auth', 'mobile', 'pro', 'sig', 'city', 'tags']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_user(account, password, mobile):
        with db.auto_commit():
            user = User()
            user.account = account
            user.nickname = account
            user.password = password
            user.mobile = mobile
            db.session.add(user)

    @staticmethod
    def verify(account, password):
        user = User.query.filter_by(account=account).first()
        if not user:
            raise NotFound(msg='用户不存在')
        if not user.check_password(password):
            raise AuthFailed(msg='密码错误')
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)

    @staticmethod
    def register_by_user_wx(openid):
        """ 用户登录向数据库增加一条用户数据 """
        with db.auto_commit():
            user = User()
            user.openid = openid
            # 将user添加到session中
            db.session.add(user)

    @staticmethod
    def update_user_msg(uid, nickname, avatar, gender, pro, sig, country, mobile, geographic):
        with db.auto_commit():
            user = User.query.filter_by(id=uid).first_or_404()
            if nickname:
                user.nickname = nickname
            if avatar:
                user.avatar = avatar
            if gender:
                user.gender = gender
            if pro:
                user.pro = pro
            if sig:
                user.sig = sig
            if country:
                user.country = country
            if mobile:
                user.mobile = mobile
            if geographic:
                city = geographic['city']
                city = ",".join(list(city.values()))
                user.city = city
                province = geographic['province']
                province = ",".join(list(province.values()))
                user.province = province

    @staticmethod
    def put_user_new_tag(title, id):
        """ 创建一个新的标签 """
        with db.auto_commit():
            user = User.query.filter_by(id=id).first()
            tags = [] if user['tags'] is None else user['tags'].split(",")
            tags.append(title)
            newtags = ",".join(tags)
            user.tags = newtags

    @staticmethod
    def batches_delete_user(ids):
        with db.auto_commit():
            users = User.query.filter(User.id.in_(ids)).delete()
