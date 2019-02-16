# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 6:55
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from app.models.message import Message
from app.models.user import User


class MessageViewModel:

    @classmethod
    def get_user_messages(cls, tid):
        unreadMessages = Message.query.filter_by(tuid=tid, read_staus=0).all()
        readMessages = Message.query.filter_by(tuid=tid, read_staus=1).all()
        totalcount = Message.query.filter_by(tuid=tid).count()
        return {
            "unread_messages": [cls.cut_user_message(item) for item in unreadMessages],
            "read_messages": [cls.cut_user_message(item) for item in readMessages],
            "totalcount": totalcount
        }

    @classmethod
    def cut_user_message(cls, data):
        fuid = data['fuid']
        user = User.query.filter_by(id=fuid).first()
        fu = {
            "user_name": user['nickname'],
            "user_avatar": user['avatar']
        }
        message = {
            "content": data["content"],
            "create_time": data["create_time"],
            "update_time": data["update_time"],
            "read": False,
            "id": data["id"],
            "from_user": fu
        }
        return message
