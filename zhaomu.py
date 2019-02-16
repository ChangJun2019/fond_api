# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 10:23
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 项目入口文件

from werkzeug.exceptions import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError

# 创建应用程序
app = create_app()


# 应用程序全局异常处理
@app.errorhandler(Exception)
def framework_error(e):
    # API异常
    if isinstance(e, APIException):
        return e
    # HTTP异常
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # log
        """ 如果是调试模式下返回具体错误 
            否则的话返回自定义json错误
        """
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e


# 运行应用程序
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')