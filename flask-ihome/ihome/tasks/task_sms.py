from celery import Celery
from ihome.libs.yixintong.sms import SMSSend


# 定义celery对象
celery_app = Celery("ihome", broker="redis://127.0.0.1:6379/1")


@celery_app.task
def send_sms(to, sms_data_info):
    """发送短信的异步任务"""
    ccp = SMSSend()
    result = ccp.send_message_info(to, sms_data_info)


# 启动 celery -A ihome.tasks.task_sms worker -l info
