# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 10:24
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 创建应用程序


from .app import Flask
from flask_cors import CORS


def register_blueprints(app):
    """ 注册蓝图到flask核心对象,并对该蓝图对象进行url前缀的设置
    """
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix="/v1")


def register_plugin(app):
    """ 注册数据模型 """
    from app.models.base import db
    # 注册插件
    db.init_app(app)
    """ 创建所有的表
    db.create_all方法必须在上下文的环境下
    使用with app_context将推入到上下文的栈中去
    """
    with app.app_context():
        db.create_all()


def create_app():
    """ 创建应用程序 """
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    # 将配置项装载到flask核心对象中
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    register_blueprints(app)
    register_plugin(app)
    return app
