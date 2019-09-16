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
        return 'http://' + ip + ':8080' + '/job/滨海农商/allure/'

    def sendDingDing(self, case_num, success_num, error_num):
        url = 'https://oapi.dingtalk.com/robot/send?access_token=148e499b4c569a472798fa84fab2437c81b9803a4edb0b5263bea340811c4ec1'
        program = {
            "msgtype": "text",
            "text": {
                "content":
                "滨海农商接口自动化运行结果:" + "\n" + str(self.get_report_url()) + "\n" +
                "运行测试用例:" + str(case_num) + "\n" + "成功:" + str(success_num) +
                "\n" + "失败:" + str(error_num)
            },
        }
        headers = {'Content-Type': 'application/json'}
        requests.post(url, data=json.dumps(program), headers=headers)


if __name__ == '__main__':
    SendDingDing().sendDingDing()
