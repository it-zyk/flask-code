from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from ihome.utils.response_code import RET
import functools

# 定义正则转换器


class ReConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        # 调用父类的初始化
        super(ReConverter, self).__init__(url_map)
        # 保存正则表达式
        self.regex = regex
