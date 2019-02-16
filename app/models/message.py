# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 5:45
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 消息表

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.models.base import Base, db
from sqlalchemy.orm import relationship
from datetime import datetime


class Message(Base):
    """ 消息数据模型 """
    id = Column(Integer, primary_key=True)  # id
    fuid = Column(Integer)  # 来自用户id
    user = relationship('User')
    tuid = Column(Integer, ForeignKey('user.id'))  # 发送给用户id
    content = Column(String(50))  # 发送内容
    read_staus = Column(Integer, default=0)  # 0未读 1已读
    update_time = Column(Integer, default=int(datetime.now().timestamp()))  # 更新时间

    def keys(self):
        return ['id', 'fuid', 'tuid', 'content', 'read_staus', 'update_time']

    @staticmethod
    def create_by_message(form, uid):
        """ 创建消息 """
        tuid = form.tuid.data
        content = form.content.data
        with db.auto_commit():
            message = Message()
            message.tuid = tuid
            message.content = content
            message.fuid = uid
            db.session.add(message)

    @staticmethod
    def change_message_status(id):
        """ 改变消息的的读取状态 """
        with db.auto_commit():
            message = Message.query.filter_by(id=id).first()
            message.read_staus = 1
            message.update_time = int(datetime.now().timestamp())
