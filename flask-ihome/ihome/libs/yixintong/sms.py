from suds.client import Client


SMS_URL = "http://10.2.8.108/SMSServices/SMSWebServices.asmx?wsdl"


class SMSSend(object):
    # 保存对象类属性

    instance = None

    def __new__(cls):
        if cls.instance is None:
            obj = super(SMSSend, cls).__new__(cls)
            obj.client = Client(SMS_URL)

            cls.instance = obj
        return cls.instance

    def send_message_info(self, to, datas):
        result = self.client.service.SendMessageInfo(to, datas)

        if result == "success":
            # 发送成功
            return 0
        else:
            # 发送失败
            return -1


if __name__ == "__main__":
    ccp = SMSSend()
    ccp.send_message_info("18622209838", "test")
