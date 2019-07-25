# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 1:55 PM
# @Author  : XuChen
# @File    : dd_module.py
import socket

import requests
import json


class SendDingDing:
    def get_report_url(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return 'http://' + ip + ':8080' + '/job/jch-api/allure/'

    def sendDingDing(self):
        url = 'https://oapi.dingtalk.com/robot/send?access_token=00eaa883c32dcc023a95b4ee84045659e2ddd8a8d5a98233cb0e2809d33c5f3d'
        program = {
            "msgtype": "text",
            "text": {
                "content": "金城银行接口自动化运行结果:" + "\n" + str(self.get_report_url())
            },
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=json.dumps(program), headers=headers)


if __name__ == '__main__':
    SendDingDing().sendDingDing()
