# -*- coding: utf-8 -*-
# @Time     : 2018/8/21 22:51
# @Author   : ChangJun
# @Email    : 52chinaweb@gmail.com
# @Function ：


from app.libs.error import APIException


class Success(APIException):
    """ 服务器响应成功 """
    code = 201  # 新增一个资源成功
    msg = 'ok'
    error_code = 0


class GetSuccess(Success):
    code = 200
    error_code = 0


class PutSuccess(Success):
    """ 修改一个资源成功 """
    code = 200
    error_code = 0


class DeleteSuccess(Success):
    """ 服务器删除操作成功 """
    code = 202
    error_code = 1


class ServerError(APIException):
    """ 服务器异常 """
    code = 500
    msg = 'sorry, we made a mistake'
    error_code = 999


class ClientTypeError(APIException):
    """ 客户端类型错误 """
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    """ 请求参数错误 """
    code = 400
    msg = '请求参数错误'
    error_code = 1000


class MobileException(APIException):
    """ 手机号已被绑定 """
    code = 400
    msg = '手机号已经被绑定'
    error_code = 1100


class NotFound(APIException):
    """ 资源未找到 """
    code = 404
    msg = 'the resource are not_found'
    error_code = 1001


class AuthFailed(APIException):
    """ 授权失败 """
    code = 401
    msg = 'Authorization failure'
    error_code = 1005


class Forbidden(APIException):
    """ 禁止访问,没有权限 """
    code = 403
    error_code = 1004
    msg = 'forbidden,not in scope'
