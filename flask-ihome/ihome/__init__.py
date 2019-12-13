from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import redis
import logging
from flask_wtf import CSRFProtect
# 数据库
db = SQLAlchemy()
# 创建redis 连接对象
redis_store = None


# 工厂模式
def create_app(config_name):
    """
    创建Flask的应用对象
    ：param config_name :str 配置模式的名字 ["develop","product"]
    :rturn:
    """
    app = Flask(__name__)

    # 根据配置模式的名字获取配置参数的类：
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 创建数据redis 连接对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST,
                                    port=config_class.REDIS_PORT)

    # 利用flask_session,将session 数据保存到redis中
    Session(app)

    # 为flask补充csrf防护
    CSRFProtect(app)

    # 为flask 添加自定义转换器
    # app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    from ihome import api_1_0
    app.register_blueprint(api_1_0.api, url_prefix="/api/v1.0")
    #
    # # 注册静态文件蓝图
    # from ihome import web_html
    # app.register_blueprint(web_html.html)
    return app
