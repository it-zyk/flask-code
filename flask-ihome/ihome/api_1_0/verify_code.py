from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store, constants
from flask import current_app, jsonify, make_response, request
from ihome.utils.response_code import RET
from ihome.models import User
from ihome.libs.yixintong.sms import SMSSend
import random
from ihome.tasks.task_sms import send_sms




@api.route("/image_codes/<image_code_id>")
def get_image_code(image_code_id):
    """
    获取图片验证
    :params image_code_id: 图片验证码编号
    ;return 验证图片
    """
    # 1.获取参数

    # 2. 检验参数
    # 3. 业务逻辑处理
    # a.生产验证码图片
    name, text, image_data = captcha.generate_captcha()
    """
    # b.将验证码真实值与编号保存在redis 中,设置有效期
    # Redis： string, list, hash, set, zset
    # "image_code":{"编号1":"真实文本”， "id2":"",} hash : hset("image_code",
    # "id1"
    # 单条维护记录，选用字符串

    # "image_code_编号" : "真实值"
    # redis_store.set("image_code_%s" % image_code_id, text)
    # redis_store.expire("image_code_%s" % image_code_id,
    # constants.IMAGE_CODE_REDIS_EXPIRES)  # 3分钟有效期
    """
    try:
        redis_store.setex("image_code_%s" % image_code_id,
                          constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(error=RET.DBERR, errmsg="保存图片验证码失败")

    # 4.返回图片
    resp = make_response(image_data)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
