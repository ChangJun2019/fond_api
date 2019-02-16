# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 17:54
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 评论
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import CommentsToPosts, LikeCommentsStatus
from app.models.comments import Comments
from app.models.like_comments import like_comments

api = Redprint('review')


@api.route('', methods=["PUT"])
@auth.login_required
def review_to_posts():
    """创建评论"""
    form = CommentsToPosts().validate_for_api()
    Comments.create_by_comments(form.pid.data, form.content.data, form.uid.data, form.tuid.data)
    return Success()


@api.route('/like', methods=['POST'])
@auth.login_required
def like_to_comments():
    form = LikeCommentsStatus().validate_for_api()
    like_comments.like_to_comments(form.pid.data, form.cid.data, form.uid.data)
    return Success()
