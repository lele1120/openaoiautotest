# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 1:55 PM
# @Author  : XuChen
# @File    : dd_module.py
import requests
import json
import socket


class SendDingDing:
    def get_report_url(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return 'http://' + ip + ':8080' + '/job/实名认证自动化测试/allure/'

    def sendDingDing(self, case_num, success_num, error_num):
        url = 'https://oapi.dingtalk.com/robot/send?access_token=3b573a9ed0156e6c4cae02b49a7ffe27be0f5e7d0c27bb96bd9edbca25e06fe1'
        program = {
            "msgtype": "text",
            "text": {
                "content":
                "实名认证接口自动化运行结果:" + "\n" + str(self.get_report_url()) + "\n" +
                "运行测试用例:" + str(case_num) + "\n" + "成功:" + str(success_num) +
                "\n" + "失败:" + str(error_num)
            },
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=json.dumps(program), headers=headers)


if __name__ == '__main__':
    SendDingDing().sendDingDing()
