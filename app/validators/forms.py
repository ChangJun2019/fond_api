# -*- coding: utf-8 -*-
# @Time    : 2018/12/06 10:24
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com
# @desc    : 项目参数验证

from wtforms import StringField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, length, Regexp
from wtforms import ValidationError
from app.validators.base import BaseForm as Form
from app.models.user import User
from app.models.topic_types import Topics
from app.models.posts import Posts


class RegisterUserForm(Form):
    """ 注册表单验证 """
    account = StringField(validators=[DataRequired(message='用户名不能为空'), length(min=2, max=25)])
    # 密码只能包含字母、数字和“_”
    password = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码格式不正确')])
    mobile = IntegerField(validators=[DataRequired(), Regexp(r'1[3,4,5,7,8]\d{9}', message='手机号格式不正确')])
    captcha = IntegerField(validators=[DataRequired(message='验证码不能为空')])

    def validate_account(self, value):
        """ 查询用户名是否重复 """
        if User.query.filter_by(account=value.data).first():
            raise ValidationError(message='用户名已重复')


class LoginUserForm(Form):
    """ 账号登陆方式表单验证 """
    account = StringField(validators=[DataRequired(message='用户名不能为空'), length(min=2, max=25)])
    # 密码只能包含字母、数字和“_”
    password = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码格式不正确')])


class LoginWxForm(Form):
    """ 微信登录方式表单验证 """
    code = StringField(validators=[DataRequired(message='登录凭证不能为空')])


class GetAllUsers(Form):
    """ 获取全部的用户信息 """
    page = IntegerField(default=1)
    per_page = IntegerField(default=10)
    nickname = StringField()
    gender = StringField()
    auth = IntegerField()


class CreateNewTopics(Form):
    """ 创建新的主题表单验证 """
    topic_name = StringField(validators=[DataRequired(message='主题名称不能为空')])
    cover = StringField(validators=[DataRequired(message='主题封面不能为空')])
    desc = StringField(validators=[DataRequired(message='主题简介不能为空')])
    parent_id = StringField()

    def validate_name(self, value):
        if Topics.query.filter_by(topic_name=value.data).first():
            raise ValidationError(message='主题名称不能重复')


class UpdateTopicsMsg(Form):
    """ 修改分类信息 """
    id = StringField(validators=[DataRequired(message='要修改的分类id不能为空')])
    topic_name = StringField()
    cover = StringField()
    desc = StringField()

    def validate_name(self, value):
        if Topics.query.filter_by(topic_name=value.data).first():
            raise ValidationError(message='主题名称不能重复')


class UpdateUserMsg(Form):
    """ 修改用户信息 """
    nickname = StringField()
    avatar = StringField()
    gender = StringField()
    pro = StringField()
    sig = StringField()
    mobile = StringField()
    country = StringField()
    geographic = StringField()


class SetUserAuth(Form):
    id = IntegerField(validators=[DataRequired(message='用户id不能为空')])


class CreatePosts(Form):
    """ 创建帖子验证 """
    title = StringField(validators=[DataRequired(message='标题不能为空')])
    sort = IntegerField(validators=[DataRequired(message='要发布的主题不能为空')])
    type = IntegerField(validators=[DataRequired(message='发布的类型是')])
    desc = StringField()
    atype = IntegerField()
    video = StringField()
    cover = StringField()
    images = StringField()
    content = StringField(validators=[DataRequired(message='要发布的内容不能为空')])

    def validate_title(self, value):
        if Posts.query.filter_by(title=value.data).first():
            raise ValidationError(message='帖子标题已存在')


class FollowedTopics(Form):
    """ 关注主题 """
    id = IntegerField(validators=[DataRequired(message='要关注的主题id不能为空')])


class FollowedUsers(Form):
    """ 关注主题 """
    id = IntegerField(validators=[DataRequired(message='要关注的主题id不能为空')])


class CollectingPosts(Form):
    """ 收藏文章 """
    id = IntegerField(validators=[DataRequired(message='要收藏的文章id不能为空')])


class GetCurrentUserAllPosts(Form):
    """ 获取当前用户所有的文章 """
    page = IntegerField(default=1)
    per_page = IntegerField(default=10)


class AddUserTags(Form):
    """ 添加用户标签 """
    tag_title = StringField(validators=[DataRequired(message='标签内容不能为空')])


class DeleteInBatches(Form):
    """ 批量删除用户 """
    idTuple = StringField()


class DeleteInBatchesByPosts(Form):
    """ 批量删除用户 """
    idTuple = StringField()


class GetAllPostsArticles(Form):
    """ 获取全部的文章 """
    page = IntegerField(default=1)
    per_page = IntegerField(default=10)
    atype = IntegerField()  # 文章类型 原创、翻译、转载
    title = StringField()  # 文章标题
    desc = StringField()  # 文章简介
    tid = IntegerField()  # 所属主题
    good = IntegerField()  # 是否是精品
    top = IntegerField()  # 是否在首位推荐


class GetALLPostsStates(Form):
    """ 获取全部的动态 """
    page = IntegerField(default=1)
    per_page = IntegerField(default=10)
    title = StringField()  # 动态标题
    tid = IntegerField()  # 所属主题
    content = StringField()  # 内容
    good = IntegerField()  # 是否是精品
    top = IntegerField()  # 是否在首位推荐


class GetALLPostsVideoStates(Form):
    """ 获取全部的视频动态 """
    page = IntegerField(default=1)
    per_page = IntegerField(default=10)
    title = StringField()  # 动态标题
    tid = IntegerField()  # 所属主题
    content = StringField()  # 内容
    good = IntegerField()  # 是否是精品
    top = IntegerField()  # 是否在首位推荐


class CommentsToPosts(Form):
    """ 评论内容 """
    pid = IntegerField(validators=[DataRequired(message="评论的帖子不能为空")])
    content = StringField(validators=[DataRequired(message="评论的内容不能为空")])
    uid = IntegerField(validators=[DataRequired(message="评论人不能为空")])
    tuid = IntegerField()


class CreateNewMessage(Form):
    """ 创建消息内容 """
    tuid = IntegerField(validators=[DataRequired(message="发送给谁不能为空")])
    content = StringField(validators=[DataRequired(message="发送消息的主题不能为空")])


class ChangeMessageStatus(Form):
    """ 修改消息状态 """
    id = IntegerField(validators=[DataRequired(message="消息id不能为空")])


class LikeCommentsStatus(Form):
    """ 给评论点赞 """
    pid = IntegerField(validators=[DataRequired(message="评论的帖子不能为空")])
    cid = IntegerField(validators=[DataRequired(message="评论id不能为空")])
    uid = IntegerField(validators=[DataRequired(message="用户id不能为空")])


class DeletePosts(Form):
    """ 删除某一篇内容 """
    id = IntegerField(validators=[DataRequired(message="要删除的帖子不能为空")])


class ChangePostsArticles(Form):
    """ 对文章进行修改 """
    id = IntegerField(validators=[DataRequired(message='id不能为空')])
    title = StringField()
    desc = StringField()
    content = StringField()


class ChangePostsIsGood(Form):
    id = IntegerField(validators=[DataRequired(message='id不能为空')])


class GetVerifyCode(Form):
    """ 获取验证码 """
    mobile = StringField(validators=[DataRequired(message='手机号不能为空')])


class VerifyCode(Form):
    """ 验证手机验证码 """
    code = StringField(validators=[DataRequired(message='验证码不能为空')])


class getArticlesOne(Form):
    """ 验证手机验证码 """
    id = IntegerField(validators=[DataRequired(message='文章id不能为空')])
