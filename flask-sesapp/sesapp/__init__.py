from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

import redis
import logging
from flask_wtf import CSRFProtect
from logging.handlers import RotatingFileHandler
from sesapp.utils.commons import ReConverter
from flask_cas import CAS

# 数据库
db = SQLAlchemy()
# 创建redis 连接对象
redis_store = None

# cas 集成
cas = CAS()

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级

# 配置日志信息
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler(
    "logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter(
    '%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日记录器
logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    app = Flask(__name__)
    '''导入配置文件'''
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # 使用app初始化db
    db.init_app(app)

    # 使用app初始化cas
    cas.init_app(app)

    # 创建数据redis 连接对象
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST,
                                    port=config_class.REDIS_PORT)

    # 利用flask_session,将session 数据保存到redis中
    Session(app)

    # 为flask补充csrf防护
    CSRFProtect(app)

    # 为flask 添加自定义转换器
    app.url_map.converters["re"] = ReConverter

    # 注册蓝图
    from sesapp import exam_v_1
    app.register_blueprint(exam_v_1.exam, url_prefix="/exam/v1.0")
    #

    # # 注册静态文件蓝图
    from sesapp import web_html
    app.register_blueprint(web_html.html)

    return app
