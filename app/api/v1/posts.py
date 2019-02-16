# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 13:21
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :
from flask import g, jsonify

from app.libs.error_code import Success, DeleteSuccess, PutSuccess
from app.libs.redprint import Redprint
from app.validators.forms import CreatePosts, GetCurrentUserAllPosts, CollectingPosts, GetAllPostsArticles, \
    GetALLPostsStates, GetALLPostsVideoStates, DeleteInBatchesByPosts, ChangePostsArticles, getArticlesOne
from app.models.posts import Posts
from app.models.collect_posts import collect_posts
from app.libs.token_auth import auth
from app.view_models.posts import PostsViewModels
from app.models.base import db

api = Redprint('posts')


@api.route('', methods=['POST'])
@auth.login_required
def create_posts():
    """ 创建一个帖子 """
    uid = g.user.uid
    form = CreatePosts().validate_for_api()
    Posts.create_by_posts(form, uid)
    posts = Posts.query.filter_by(title=form.title.data).first()
    pid = {
        "posts_id": posts.id  # 返回创建好的分类id
    }
    return Success(msg=pid)


@api.route('/article', methods=['POST'])
@auth.login_required
def get_posts_one_articles():
    """ 获取某一篇文章 """
    form = getArticlesOne().validate_for_api()
    articles = Posts.query.filter_by(type=1, id=form.id.data).first()
    articles = PostsViewModels.cut_get_my_articles(articles)
    return jsonify(articles)


@api.route('/statesone', methods=['POST'])
@auth.login_required
def get_posts_one_states():
    """ 获取某一篇动态 """
    form = getArticlesOne().validate_for_api()
    states = Posts.query.filter_by(type=2, id=form.id.data).first()
    states = PostsViewModels.cut_get_my_states(states)
    return jsonify(states)


@api.route('/vstatesone', methods=['POST'])
@auth.login_required
def get_posts_one_vstates():
    """ 获取某一篇视频动态 """
    form = getArticlesOne().validate_for_api()
    vstates = Posts.query.filter_by(type=3, id=form.id.data).first()
    vstates = PostsViewModels.cut_get_my_vstates(vstates)
    return jsonify(vstates)


@api.route('/articles/all', methods=['POST'])
@auth.login_required
def get_topics_all():
    """ 获取当前用户发布的所有文章（分页） """
    uid = g.user.uid
    form = GetCurrentUserAllPosts().validate_for_api()
    articles = Posts.query.filter_by(uid=uid, type=1).paginate(page=form.page.data, per_page=form.per_page.data,
                                                               error_out=False)
    articles = PostsViewModels.paginate_user_all_articles(articles)
    return jsonify(articles)


@api.route("/articles", methods=['POST'])
@auth.login_required
def get_all_posts_articles():
    """ 获取所有的帖子 """
    form = GetAllPostsArticles().validate_for_api()
    articles = get_posts_all_articles(form)
    articles = PostsViewModels.paginate_all_articles(articles)
    return jsonify(articles)


@api.route("/states", methods=["POST"])
@auth.login_required
def get_all_posts_states():
    """ 获取所有的动态 """
    form = GetALLPostsStates().validate_for_api()
    states = get_posts_all_states(form)
    states = PostsViewModels.paginate_all_states(states)
    return jsonify(states)


@api.route("/vstates", methods=["POST"])
@auth.login_required
def get_all_posts_video_states():
    """ 获取所有的视频动态 """
    form = GetALLPostsVideoStates().validate_for_api()
    videostates = get_posts_all_video_states(form)
    videostates = PostsViewModels.paginate_all_video_states(videostates)
    return jsonify(videostates)


@api.route('/articles', methods=['GET'])
@auth.login_required
def get_user_posts_all():
    """ 获取当前用户发布的所有文章（不分页）"""
    uid = g.user.uid
    articles = Posts.query.filter_by(uid=uid, type=1).all()
    articles = PostsViewModels.get_all_posts_articles(articles)
    return jsonify(articles)


@api.route('/states', methods=['GET'])
@auth.login_required
def get_user_posts_state_all():
    """ 获取当前用户发布的所有动态 """
    uid = g.user.uid
    states = Posts.query.filter_by(uid=uid, type=2).all()
    states = PostsViewModels.get_all_posts_states(states)
    return jsonify(states)


@api.route('/vstates', methods=['GET'])
@auth.login_required
def get_user_posts_video_all():
    """ 获取当前用户发布的所有视频动态 """
    uid = g.user.uid
    vstates = Posts.query.filter_by(uid=uid, type=3).all()
    vstates = PostsViewModels.get_all_posts_vstates(vstates)
    return jsonify(vstates)


@api.route('/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_by_posts(id):
    """ 删除一个动态 """
    with db.auto_commit():
        post = Posts.query.filter_by(id=id).first_or_404()
        post.delete()
    return DeleteSuccess()


@api.route('/delete', methods=['POST'])
@auth.login_required
def delete_by_posts_batches():
    """ 批量删除动态 """
    form = DeleteInBatchesByPosts().validate_for_api()
    ids = tuple(form.idTuple.data)
    with db.auto_commit():
        posts = Posts.query.filter(Posts.id.in_(ids))
        [post.delete() for post in posts]
    return DeleteSuccess()


@api.route('/collecting', methods=['POST'])
@auth.login_required
def collectiong_posts():
    """ 收藏内容 """
    uid = g.user.uid
    form = CollectingPosts().validate_for_api()
    collect_posts.collecting_posts(form.id.data, uid)
    return Success()


@api.route('/changed', methods=['PUT'])
@auth.login_required
def update_posts_by_articles():
    """ 修改文章 """
    form = ChangePostsArticles().validate_for_api()
    with db.auto_commit():
        posts = Posts.query.filter_by(id=form.id.data).first_or_404()
        if form.title.data:
            posts.title = form.title.data
        if form.desc.data:
            posts.desc = form.desc.data
        if form.content.data:
            posts.content = form.content.data
    return PutSuccess()


@api.route('/good/<int:id>', methods=['PUT'])
@auth.login_required
def update_posts_good(id):
    """ 修改是否精品 """
    with db.auto_commit():
        posts = Posts.query.filter_by(id=id).first_or_404()
        posts.good = 1 if posts.good == 0 else 0
    return PutSuccess()


@api.route('/top/<int:id>', methods=['PUT'])
@auth.login_required
def update_posts_top(id):
    """ 修改是否推荐 """
    with db.auto_commit():
        posts = Posts.query.filter_by(id=id).first_or_404()
        posts.top = 1 if posts.top == 0 else 0
    return PutSuccess()


def get_posts_all_articles(form):
    """ 获取所有的文章 """
    posts = Posts.query.filter_by(type=1)
    if form.atype.data:
        posts = Posts.query.filter_by(atype=form.atype.data, type=1)
    if form.tid.data:
        posts = Posts.query.filter_by(tid=form.tid.data, type=1)
    if form.good.data:
        posts = Posts.query.filter_by(good=form.good.data, type=1)
    if form.top.data:
        posts = Posts.query.filter_by(top=form.top.data, type=1)
    if form.atype.data and form.tid.data and form.good.data and form.top.data:
        posts = Posts.query.filter_by(atype=form.atype.data, tid=form.tid.data, good=form.good.data, top=form.top.data)
    title_words = form.title.data.strip() if form.title.data else ""
    desc_words = form.desc.data.strip() if form.desc.data else ""
    posts = posts.filter(Posts.title.like("%" + title_words + "%"), Posts.desc.like("%" + desc_words + "%")).paginate(
        page=form.page.data,
        per_page=form.per_page.data,
        error_out=False)
    return posts


def get_posts_all_states(form):
    """ 获取所有的动态 """
    posts = Posts.query.filter_by(type=2)
    if form.tid.data:
        posts = Posts.query.filter_by(tid=form.tid.data, type=2)
    if form.good.data:
        posts = Posts.query.filter_by(good=form.good.data, type=2)
    if form.top.data:
        posts = Posts.query.filter_by(top=form.top.data, type=2)
    if form.tid.data and form.good.data and form.top.data:
        posts = Posts.query.filter_by(tid=form.tid.data, good=form.good.data, top=form.top.data)
    title_words = form.title.data.strip() if form.title.data else ""
    content_words = form.content.data.strip() if form.content.data else ""
    posts = posts.filter(Posts.title.like("%" + title_words + "%"),
                         Posts.content.like("%" + content_words + "%")).paginate(
        page=form.page.data,
        per_page=form.per_page.data,
        error_out=False)
    return posts


def get_posts_all_video_states(form):
    """ 获取所有的视频动态 """
    posts = Posts.query.filter_by(type=3)
    if form.tid.data:
        posts = Posts.query.filter_by(tid=form.tid.data, type=3)
    if form.good.data:
        posts = Posts.query.filter_by(good=form.good.data, type=3)
    if form.top.data:
        posts = Posts.query.filter_by(top=form.top.data, type=3)
    if form.tid.data and form.good.data and form.top.data:
        posts = Posts.query.filter_by(tid=form.tid.data, good=form.good.data, top=form.top.data)
    title_words = form.title.data.strip() if form.title.data else ""
    content_words = form.content.data.strip() if form.content.data else ""
    posts = posts.filter(Posts.title.like("%" + title_words + "%"),
                         Posts.content.like("%" + content_words + "%")).paginate(
        page=form.page.data,
        per_page=form.per_page.data,
        error_out=False)
    return posts
