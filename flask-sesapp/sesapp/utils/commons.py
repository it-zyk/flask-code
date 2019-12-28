from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from sesapp.utils.response_code import RET


import functools


class ReConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        # 调用父类的初始化
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex


# 定义的验证登录状态的装饰器
def login_required(view_func):
    # wraps函数的作用是将wrapper内层函数的属性设置为被装饰函数view_func的属性
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        # user_id = session.get("user_id")
        from sesapp import cas
        username = cas.username
        # 如果用户是登录的， 执行视图函数
        if username is not None:
            # 将username保存到g对象中，在视图函数中可以通过g对象获取保存数据
            g.username = username
            return view_func(*args, **kwargs)
        else:
            # 如果未登录，返回未登录的信息
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    return wrapper
